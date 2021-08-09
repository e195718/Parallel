import time
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

def make_complex(re, im): #複素数作成
    Re, Im = np.meshgrid(re, im)
    comp = np.c_[Re.ravel(), Im.ravel()]
    return comp

def make_figure(obj): #画像生成
    fig = plt.figure(dpi=600)
    plt.axis("off")
    plt.imshow(obj, cmap="bone", extent=[-2, 2, -2, 2])
    fig.set_size_inches(1.5, 1.5)
    return plt.show()

def check_julia(comp, n_loops=200, threshold=2): #ジュリア集合作成
    """
    c = -0.7 - 0.3i
    """
    re, im = comp[0], comp[1]
    c = complex(-0.7, -0.3)
    z = complex(re, im) #実部がre、虚部がim

    for i in range(n_loops):
        z = z*z + c
        if abs(z) >= threshold:
            return i        
    return n_loops

def sub_check_julia(comp): #ジュリア集合に属するかチェック
    comp_list = []
    for c_point in comp:
        comp_list.append(check_julia(c_point))

    return comp_list

def measure(n_para, separate): #並列化を行う
    re = np.linspace(-2, 2, 2000)
    im = np.linspace(2, -2, 2000)
    comp = make_complex(re, im)

    sep_comp = len(comp) // separate
    result = []
    for y in range(separate):
        result.append(comp[sep_comp * y : sep_comp * (y+1)])

    pool = mp.Pool(n_para)
    s_time = time.time()
    cb = pool.map(sub_check_julia, result)
    e_time = time.time()
    print("time: {0:.3f}[s]".format(e_time - s_time))

    mp_result = []

    for i in cb:
        mp_result.extend(i)

    Julia = np.array(mp_result)

    Julia = Julia.reshape((2000, 2000))
    
    return make_figure(Julia)

if __name__ == "__main__":
    n_para = 8
    separate = 10
    cb = measure(n_para, separate)