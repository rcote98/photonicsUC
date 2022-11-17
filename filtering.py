#!/usr/bin/python3

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

## DEFAULTS ###########################

global SRC
SRC = "img/dog.jpg" # image source file
global IMG
IMG = np.zeros(1) # image to work on
global P_SPACING
P_SPACING = 40 # spacing for positive filters
global N_SPACING
N_SPACING = 15 # spacing for negative filters
global SIGMA
SIGMA = 10 # sigma value for gaussian filters

#######################################
## FILTER STUFF #######################

def apply_filter(image, filtr):

    """Applies the filter to the image."""

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    masked = np.multiply(filtr, fshift)

    fishift = np.fft.ifftshift(masked)

    res = np.fft.ifft2(fishift)

    return np.abs(res)


def low_pass_filter(image, fsize):

    """Creates a low-pass square filter 
    (eliminates high frequencies)
    for the given image."""

    H, W = np.shape(image)
    mW = int(np.fix(0.5*W))
    mH = int(np.fix(0.5*H))   

    side = fsize
    mask = np.zeros((H,W))
    mask[mH-side:mH+side,mW-side:mW+side] = 1

    return mask

def gaussian_filter(image, sigma, negative = False):

    """Creates a high/low-pass gaussian filter 
    for the given image."""

    H, W = np.shape(image)
    mW = int(np.fix(0.5*W))
    mH = int(np.fix(0.5*H))   

    mask = np.zeros((H,W))

    for i in range(H):
        for j in range(W):
            mask[i,j] = np.exp(-((i-mH)**2/(2.*sigma**2.) + (j-mW)**2./(2.* sigma**2.)))

    mask = mask/np.max(mask)

    if negative:
        return 1 - mask
    else:
        return mask


def high_pass_filter(image, fsize):

    """Creates a high-pass square filter 
    (eliminates low frequencies)
    for the given image."""

    H, W = np.shape(image)
    mW = int(np.fix(0.5*W))
    mH = int(np.fix(0.5*H))   

    side = fsize
    mask = np.ones((H,W))
    mask[mH-side:mH+side,mW-side:mW+side] = 0

    return mask

def horizontal_filter(image, fsize, negative=False):

    """Creates a horizontal band filter 
    for the given image."""

    H, W = np.shape(image)
    mH = int(np.fix(0.5*H))   

    if negative:
        side = fsize
        mask = np.ones((H,W))
        mask[mH-side:mH+side,:] = 0
    else:
        side = fsize
        mask = np.zeros((H,W))
        mask[mH-side:mH+side,:] = 1

    return mask

def vertical_filter(image, fsize, negative=False):

    """Creates a vertical band filter 
    for the given image."""

    H, W = np.shape(image)
    mW = int(np.fix(0.5*W))   

    if negative:
        side = fsize
        mask = np.ones((H,W))
        mask[:,mW-side:mW+side] = 0
    else:
        side = fsize
        mask = np.zeros((H,W))
        mask[:,mW-side:mW+side] = 1

    return mask

#######################################

def plot_stuff(image, filtr, result):

    plt.figure(figsize=(900, 400))

    plt.subplot(1,3,1)
    plt.title("Image", fontsize=16)
    plt.imshow(image, cmap="gray")

    plt.subplot(1,3,2)
    plt.title("Filter", fontsize=16)
    plt.imshow(filtr, cmap="gray")

    plt.subplot(1,3,3)
    plt.title("Filtered Image", fontsize=16)
    plt.imshow(result, cmap="gray")

    plt.show()

#######################################
## MENU ###############################

def menu():

    print("")
    print("### FOURIER TRANSFORM FILTERING ### ")
    print("")
    print("Raúl Coterillo")
    print("")
    print("This program applies one of several filters") 
    print("to an image using the Fourier transform method.")
    print("For more details, please refer to the source code.")
    print("")

    global SRC
    rply = input_def("Please, input the image file: (default: " + SRC + ")", SRC)
    SRC = rply

    try:
        global IMG
        IMG = np.array(Image.open(rply).convert("L"))
    except FileNotFoundError:
        print("\n File does not exist, quitting.")
        quit()
    except OSError:
        print("\n File type not recognized, quitting.")
        quit()
    

    print("Next, select the filter to apply: (default: High-pass)")
    print("[1] - High-pass")
    print("[2] - Low-pass") 
    print("[3] - Horizontal")
    print("[4] - Vertical")
    choice = input("-> ")
    print("")

    #defaulting to high-pass
    if(choice == ""):
        choice = "1"

    if choice == "1":
        
        print("Now select the type of filter: (default: Gaussian)")
        print("[1] - Gaussian")
        print("[2] - Square") 
        sh = input("-> ")

        if(sh == ""):
            sh = "1"

        if sh == "1":

            global SIGMA
            rply = input_def("Dispersion value sigma? (default:"+
                str(SIGMA)+ ")", SIGMA)
            rply = int(rply)

            print("Applying filter...")
            mask = gaussian_filter(IMG, SIGMA, negative=True)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")

            plot_stuff(IMG, mask, result)

        elif sh == "2":

            global N_SPACING
            rply = input_def("Dispersion filter size? (default:"+
                str(N_SPACING)+ ")", N_SPACING)
            rply = int(rply)

            print("Applying filter...")
            mask = high_pass_filter(IMG, N_SPACING)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")
            
            plot_stuff(IMG, mask, result)

        else:
            print("Please, input a valid number.")
            quit()


    elif choice == "2":
        
        print("Now select the type of filter: (default: Gaussian)")
        print("[1] - Gaussian")
        print("[2] - Square") 
        sh = input("-> ")

        if(sh == ""):
            sh = "1"

        if sh == "1":

            rply = input_def("Dispersion value sigma? (default:"+
                str(SIGMA)+ ")", SIGMA)
            rply = int(rply)

            print("Applying filter...")
            mask = gaussian_filter(IMG, SIGMA, negative=False)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")

            plot_stuff(IMG, mask, result)

        elif sh == "2":

            global P_SPACING
            rply = input_def("Dispersion filter size? (default:"+
                str(P_SPACING)+ ")", P_SPACING)
            rply = int(rply)

            print("Applying filter...")
            mask = low_pass_filter(IMG, P_SPACING)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")
            
            plot_stuff(IMG, mask, result)

        else:
            print("Please, input a valid number.")
            quit()

    elif choice == "3":
        
        print("Now select the type of filter: (default: Positive)")
        print("[1] - Positive (retains horizontal frequencies)")
        print("[2] - Negative (removes horizontal frequencies)") 
        sh = input("-> ")

        if(sh == ""):
            sh = "1"

        if sh == "1":

            rply = input_def("Filter width? (default:"+
                str(P_SPACING)+ ")", P_SPACING)
            P_SPACING = int(rply)

            print("Applying filter...")
            mask = horizontal_filter(IMG, P_SPACING, negative=False)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")

            plot_stuff(IMG, mask, result)

        elif sh == "2":

            rply = input_def("Filter width? (default:"+
                str(N_SPACING)+ ")", N_SPACING)
            N_SPACING = int(rply)

            print("Applying filter...")
            mask = horizontal_filter(IMG, N_SPACING, negative=True)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")
            
            plot_stuff(IMG, mask, result)

        else:
            print("Please, input a valid number.")
            quit()

    elif choice == "4":
        
        print("Now select the type of filter: (default: Positive)")
        print("[1] - Positive (retains vertical frequencies)")
        print("[2] - Negative (removes vertical frequencies)") 
        sh = input("-> ")

        if(sh == ""):
            sh = "1"

        if sh == "1":

            rply = input_def("Filter width? (default:"+
                str(P_SPACING)+ ")", P_SPACING)
            P_SPACING = int(rply)

            print("Applying filter...")
            mask = vertical_filter(IMG, P_SPACING, negative=False)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")

            plot_stuff(IMG, mask, result)

        elif sh == "2":

            rply = input_def("Filter width? (default:"+
                str(N_SPACING)+ ")", N_SPACING)
            N_SPACING = int(rply)

            print("Applying filter...")
            mask = vertical_filter(IMG, N_SPACING, negative=True)
            result = apply_filter(IMG, mask)
            print("DONE! Plotting...")
            
            plot_stuff(IMG, mask, result)

        else:
            print("Please, input a valid number.")
            quit()

    else:

        print("Please, input a valid number.")
    

def input_def(ph, def_val):

    print(ph)
    rply = input("-> ")
    print("")

    if(rply != ""):
        return rply
    else:
        return def_val



## MAIN METHOD

if __name__ == "__main__":

    """ Launch this on execute."""

    menu()
    quit()