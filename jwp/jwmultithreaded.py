import multiprocessing
from multiprocessing.pool import Pool, ThreadPool
from multiprocessing import cpu_count
import traceback
# for reference:
# from multiprocessing import Manager, Lock

cpus = cpu_count()


def multithread(fn, args=[[]], pool_type=Pool,
                processes=cpus, maxtasksperchild=1,
                chunksize=1):
    '''Multithread method using a Pool. Not inherently threadsafe.
    For threadsafe operations, use Managers or Locks.
    Args must be wrapped in their own list, as starmap is used for
    multiple arguments.
    Returns a list of the results'''

    def helper(pool):
        return pool.starmap(fn, args, chunksize=chunksize)

    # ThreadPools do not take a maxtasksperchild argument,
    # so we need to conditionally construct a pool

    if type(pool_type) is Pool:
        with pool_type(processes, maxtasksperchild=maxtasksperchild) as pool:
            results = helper(pool)
    else:
        with pool_type(processes) as pool:
            results = helper(pool)
    return results


def safe_multithread(fn, args=[[]], processes=cpus, chunksize=1):
    '''Guaranteed threadsafe version of multithread using ThreadPool.
    Allows child threads. Limited by interpreter lock.'''
    return multithread(fn, args=args, pool_type=ThreadPool, processes=processes,
                       chunksize=chunksize)


def multithread_failsafe(fn, args=[[]], pool_type=Pool,
                         processes=cpus, chunksize=1, verbose=True):
    '''Aynchronous multithreading that does not break on individual errors.
    Instead, prints error and message, and the input is disregarded'''

    def helper(pool):
        # threads = []
        # for elem in args:
        #     threads.append(pool.apply_async(fn, elem))
        results = []
        result_objs = [pool.apply_async(fn, arg) for arg in args]
        for r in result_objs:
            try:
                results.append(r.get())
            except:
                if verbose:
                    print('######BEGIN TRACEBACK######')
                    traceback.print_exc()
                    print('######END TRACEBACK######')
                    print()
        return results

    # ThreadPools do not take a maxtasksperchild argument,
    # so we need to conditionally construct a pool

    if type(pool_type) is Pool:
        with pool_type(processes) as pool:
            results = helper(pool)
    else:
        with pool_type(processes) as pool:
            results = helper(pool)

    return results


def safe_multithread_failsafe(fn, args=[[]], processes=cpus, chunksize=1, verbose=True):
    '''Threadsafe version of multithread_failsafe.
    Allows child threads. Limited by interpreter lock.'''

    return multithread_failsafe(fn, args=args, pool_type=ThreadPool,
                                processes=processes, verbose=verbose)

# http://stackoverflow.com/questions/6974695/python-process-pool-non-daemonic
# Experimental for processes that spawn children. In my experience,
# often results in broken pipes.


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.


class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


# deprecated super-class

class jwmultithreaded(object):
    '''Inspired by http://chriskiehl.com/article/parallelism-in-one-line/
    as well as operations that do not need to be threadsafe'''

    def __init__(self):
        self.cache_updated = False

    def multithread(self, fn, args=[[]], pool_type=Pool,
                    processes=cpus, maxtasksperchild=1,
                    chunksize=1):
        '''Multithread method using a Pool. Not inherently threadsafe.
        For threadsafe operations, use Managers.
        Args must be wrapped in their own list, as starmap is used for
        multiple arguments.
        Returns a list of the results'''

        def helper(pool):
            return pool.starmap(fn, args, chunksize=chunksize)

        # ThreadPools do not take a maxtasksperchild argument,
        # so we need to conditionally construct a pool

        if type(pool_type) is Pool:
            with pool_type(processes, maxtasksperchild=maxtasksperchild) as pool:
                results = helper(pool)
        else:
            with pool_type(processes) as pool:
                results = helper(pool)
        return results

    def safe_multithread(self, fn, args=[[]], processes=cpus,
                         chunksize=1):
        '''Guaranteed threadsafe version of multithread using ThreadPool.
        Allows child threads. Limited by interpreter lock.'''

        return self.multithread(fn, args=args, pool_type=ThreadPool,
                                processes=processes,
                                chunksize=chunksize)

    def multithread_failsafe(self, fn, args=[[]], pool_type=Pool,
                             processes=cpus, maxtasksperchild=1,
                             chunksize=1, verbose=True):
        '''Aynchronous multithreading that does not break on individual errors.
        Instead, prints error and message, and the input is disregarded'''

        def helper(pool):
            # threads = []
            # for elem in args:
            #     threads.append(pool.apply_async(fn, elem))
            results = []
            for r in pool.starmap_async(fn, args, chunksize=chunksize):
                try:
                    results.append(r.get())
                except:
                    if verbose:
                        print('######BEGIN TRACEBACK######')
                        traceback.print_exc()
                        print('######END TRACEBACK######')
                        print()
            return results

        # ThreadPools do not take a maxtasksperchild argument,
        # so we need to conditionally construct a pool

        if type(pool_type) is Pool:
            with pool_type(processes, maxtasksperchild=maxtasksperchild) as pool:
                results = helper(pool)
        else:
            with pool_type(processes) as pool:
                results = helper(pool)

        return results

    def safe_multithread_failsafe(self, fn, args=[[]], processes=cpus, verbose=True):
        '''Threadsafe version of multithread_failsafe.
        Allows child threads. Limited by interpreter lock.'''

        return self.multithread_failsafe(fn, args=args, pool_type=ThreadPool,
                                         processes=processes, verbose=verbose)
