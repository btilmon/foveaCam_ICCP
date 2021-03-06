import numpy as np
from matplotlib import pyplot as plt
import derivatives 

plt.rcParams["font.family"] = "Times New Roman"    
plt.rcParams.update({'font.size': 15})

edgeeffect = 0.1

I = np.zeros((1000, 1000, 1)) #imread('leftstart.png') 

sims = 0
while True:
    step = np.random.randint(1,600,1)
    bbox = np.array([step, step+50, 150, 250]) 

    M, N, P = I.shape

    lfimcentx = N/2
    lfimcenty = M/2

    xlfimo = bbox[0] + 0.5*bbox[2]
    ylfimo = bbox[1] + bbox[3]

    K1 = 1/300
    K2 = (K1*100)/N
    # % how much of sigma is the bbox dimension
    K3 = 2

    # left image
    xlfim = bbox[0] + 0.5*bbox[2] - lfimcentx
    ylfim = bbox[1] + bbox[3] - lfimcenty
    sigmaim = K3*max(bbox[2],bbox[3])

    d = 0 
    c = 0.5 - (K2*N)/2

    xlf = c - K2*xlfim
    ylf = d - K2*ylfim
    sigmal = sigmaim*K2

    x = np.zeros((1,2))
    y = np.zeros((1,2))

    x[:,1] = xlf + edgeeffect
    y[:,1] = ylf

    # right image
    step = np.random.randint(1,600,1)
    bbox = np.array([step, step+50, 150, 250]) 

    xlfimo = bbox[0] + 0.5*bbox[2]
    ylfimo = bbox[1] + bbox[3]

    xlfim = bbox[0] + 0.5*bbox[2] - lfimcentx
    ylfim = bbox[1] + bbox[3] - lfimcenty
    sigmaim = K3*max(bbox[2],bbox[3])

    b = 0 
    a = -0.5 + (K2*N)/2

    xrf = a - K2*xlfim
    yrf = b - K2*ylfim
    sigmar = sigmaim*K2

    x[:,0] = xrf -edgeeffect 
    y[:,0] = yrf

    # final right image
    step = np.random.randint(1,600,1)
    bbox = np.array([step, step+50, 150, 250]) 

    xlfimo = bbox[0] + 0.5*bbox[2]
    ylfimo = bbox[1] + bbox[3]

    xlfim = bbox[0] + 0.5*bbox[2] - lfimcentx
    ylfim = bbox[1] + bbox[3] - lfimcenty
    sigmaim = K3*max(bbox[2],bbox[3])

    b = 0 
    a = -0.5 + (K2*N)/2

    xrf = a - K2*xlfim
    yrf = b - K2*ylfim
    sigmar = sigmaim*K2

    K4a = 1/np.abs(x[:,0])
    K4b = 1/np.abs(x[:,1])

    x[:,0] = x[:,0]*K4a
    x[:,1] = x[:,1]*K4b

    y[:,0] = y[:,0]*K4a
    y[:,1] = y[:,1]*K4b

    # variance in both directions
    sigma1l, sigma2l = sigmal, sigmal
    rhol = 0
    sigma1r, sigma2r = sigmar, sigmar
    rhor = 0 # how elliptical it is

    # normalize
    X, Y = np.meshgrid(np.arange(100), np.arange(100))
    Y = np.flipud(Y)
    mX = X.mean()
    mY  = Y.mean()
    mxX = X.max()
    mxY  = Y.max()
    X = X - mX
    Y = Y - mY
    X = X / mxX
    Y = Y / mxY

    # Calculate gaussians in the image plane
    C1p = 1/sigma1l**2
    C2p = 2 * rhol / (sigma1l * sigma2l)
    C3p = 1 / sigma2l**2
    C4 = 1 / (2 * (1 - rhol**2))

    C1 = C1p / C4
    C2 = C2p / C4
    C3 = C3p / C4

    C5 = 1/(2 * np.pi * sigma1l * sigma2l * np.sqrt(1 - rhol**2))


    fgauss = C5*np.exp(-1*(C1*(X - xlf)**2 - C2*(X - xlf)*(Y - ylf) + C3*(Y - ylf)**2))


    C1pr = 1/sigma1r**2
    C2pr = 2*rhor/(sigma1r*sigma2r)
    C3pr = 1/sigma2r**2
    C4r = 1/(2*(1-rhor**2))
    C1r = C1pr / C4r
    C2r = C2pr / C4r
    C3r = C3pr / C4r
    C5r = 1/(2*np.pi*sigma1r*sigma2r*np.sqrt(1 - rhor**2))


    fgauss2 = C5r*np.exp(-1*(C1r*(X - xrf)**2 - C2r*(X - xrf)*(Y - yrf) + C3r*(Y - yrf)**2))
    fgaussd = fgauss/np.max(fgauss)
    fgauss2d = fgauss2/np.max(fgauss2)

    f = fgauss + fgauss2
    fd = fgaussd + fgauss2d

    x1t = x[:,0]
    y1t = y[:,0]
    x2t = x[:,1]
    y2t = y[:,1]
    xr = x[:,0]
    yr = y[:,0]

    alpha = np.arctan((ylf - yrf)/(xlf - xrf))#np.arctan((y2t - y1t)/(x2t - x1t))
    L = np.sqrt((x[:,1] - x[:,0])**2 + (y[:,1] - y[:,0])**2)

    plt.imshow(fd,cmap='gray')
     
    xo = xlf 
    yo = ylf 
        
    xrp = xrf*mxX + mX
    yrp = yrf*mxY + mY
    yrp = 100 - yrp

    xop = xo*mxX + mX
    yop = yo*mxY + mY
    yop = 100 - yop

    plt.plot([xrp,xop],[yrp,yop],'tab:green',marker='o', label='True')

    # used for visualization
    L_tmp = np.sqrt(((xrf) - (xlf))**2 + ((yrf) - (ylf))**2)

    # calc derivs
    struct = {'C1':C1, 'C2':C2, 'C3':C3, 'C4':C4, 'C5':C5, 
    'xlf':xlf, 'ylf':ylf, 'E':np.exp(1), 'xr':xr, 'yr':yr, 'alpha':alpha, 
    'L':L, 'C1r':C1r, 'C2r':C2r, 'C3r':C3r, 'C4r':C4r, 'C5r':C5r, 
    'xrf':xrf, 'yrf':yrf}
    derivs = derivatives.calculate(struct)

    #optimization params    
    smallval = .1
    lr = .01
    oldnorm = np.linalg.norm(derivs) + 0.01
    newnorm = oldnorm + 5

    q_r = np.array([xrf, yrf, alpha]).reshape(3,1)
    Br = np.zeros((3,2))
    u_r = np.zeros((2,1))
    dt = 0.1

    # Optimization running
    while np.abs(newnorm - oldnorm) > 0.5:
        oldnorm = np.linalg.norm(derivs)
        oldqr = q_r

        Br[0,0] = dt*np.cos(alpha)
        Br[1,0] = dt*np.sin(alpha)
        Br[2,1] = dt

        # update MEMS motion
        u_r += lr*dt*(derivs.transpose()@Br).transpose()
        q_r += Br@u_r + dt*lr*derivs
       
        # new mems location
        xr = q_r[0][0]
        yr = q_r[1][0]
        alpha = q_r[2][0]

        # new Pi location
        xo = xr + L_tmp*np.cos(alpha)
        yo = yr + L_tmp*np.sin(alpha)

        xrp = xr*mxX + mX
        yrp = yr*mxY + mY
        yrp = 100 - yrp

        xop = xo*mxX + mX
        yop = yo*mxY + mY
        yop = 100 - yop

        # compute derivatives
        struct['xr'], struct['yr'], struct['alpha'] = xr, yr, alpha
        derivs = derivatives.calculate(struct)
        newnorm = np.linalg.norm(derivs)

    plt.plot([xrp,xop],[yrp,yop],'tab:red', marker='d', label='Predicted', linewidth=2)
    q_r = np.round(q_r, 3)

    plt.legend(fontsize=10)
    plt.axis('off')
    plt.title('MEMS Tracking Simulation')#+'[x, y, alpha]: ['+str(q_r[0][0])+', '+str(q_r[0][0])+', '+str(q_r[0][0])+']')
    plt.pause(0.0000000001)
    plt.clf()
    sims += 1
plt.close()


