##Simultaneous Linear Equation:SLEを導く

import numpy as np
import time,os


def CG(A,x,b,Conv):
##Ax=bを共役勾配法で解く
    loop=0
    r=b-np.dot(A,x)
    Err=np.linalg.norm(r)
    print("ループ{:d}回目の残差={:e}".format(loop, Err))
    p=r
    start=time.time()
    cmp_time=0

    while (Err>Conv)and(cmp_time<60*15):
        loop=loop+1
        y=np.dot(A,p)
        alpha=np.dot(p,r)/np.dot(p,y)
        x=x+alpha*p
        r=r-alpha*y
        Err=np.linalg.norm(r)
        end=time.time()
        cmp_time=end-start
        if loop%10==0:print("経過時間:{:.1f}秒 ループ{:d}回目の残差={:e}".format(cmp_time, loop, Err))
        beta=-np.dot(r,y)/np.dot(p,y)
        p=r+beta*p

    if cmp_time>60*15:print("収束しませんでした")
    return x


def main():
    LX:double=1.0; #[m]
    LY:double=1.0; #[m]
    NX:int=100; #節点数
    NY:int=100;
    dX:double=LX/(NX-1);
    dY:double=LY/(NY-1);
    phi:double=np.zeros((NX,NY)); #[V]
    rho:double=np.zeros((NX,NY)); #[C/m^2]
    EPS:double=8.85e-12; #[F/m]
    A:double=np.zeros((NX*NY,NX*NY))
    b:double=np.zeros(NX*NY)
    x:double=np.zeros(NX*NY); #CGの初期値
    Conv:double=1e-6;

    ##問題設定
    for i in range(0,NX,1):
      for j in range(0,NY,1):
          if np.sqrt((0.5-i*dX)**2+(0.5-j*dY)**2)<=0.05:
              rho[i][j]=1e-8;


##Ax=bで書く
    for i in range(1,NX-1):
      for j in range(0,NY):
          if j==0:
                A[i*NX+j][(i-1)*NX+j]-=1/(dX)**2;
                A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
                A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
                A[i*NX+j][(i+1)*NX+j]-=1/(dX)**2;
                b[i*NX+j]-=-rho[i][j]/EPS;
          elif j==NY-1:
                A[i*NX+j][(i-1)*NX+j]-=1/(dX)**2;
                A[i*NX+j][i*NX+(j-1)]-=1/(dY)**2;
                A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
                A[i*NX+j][(i+1)*NX+j]-=1/(dX)**2;
                b[i*NX+j]-=-rho[i][j]/EPS;
          else:
                A[i*NX+j][(i-1)*NX+j]-=1/(dX)**2;
                A[i*NX+j][i*NX+(j-1)]-=1/(dY)**2;
                A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
                A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
                A[i*NX+j][(i+1)*NX+j]-=1/(dX)**2;
                b[i*NX+j]-=-rho[i][j]/EPS;

    i=0
    j=0
    A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
    A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
    A[i*NX+j][(i+1)*NX+j]-=1/(dX)**2;
    b[i*NX+j]-=-rho[i][j]/EPS;
    for j in range(1,NY-1):
        A[i*NX+j][i*NX+(j-1)]-=1/(dY)**2;
        A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
        A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
        A[i*NX+j][(i+1)*NX+j]-=1/(dX)**2;
        b[i*NX+j]-=-rho[i][j]/EPS;
    j=NY-1
    A[i*NX+j][i*NX+(j-1)]-=1/(dY)**2;
    A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
    A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
    A[i*NX+j][(i+1)*NX+j]-=1/(dX)**2;
    b[i*NX+j]-=-rho[i][j]/EPS;

    i=NX-1
    j=0
    A[i*NX+j][(i-1)*NX+j]-=1/(dX)**2;
    A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
    A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
    b[i*NX+j]-=-rho[i][j]/EPS;
    for j in range(1,NY-1):
        A[i*NX+j][(i-1)*NX+j]-=1/(dX)**2;
        A[i*NX+j][i*NX+(j-1)]-=1/(dY)**2;
        A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
        A[i*NX+j][i*NX+(j+1)]-=1/(dY)**2;
        b[i*NX+j]-=-rho[i][j]/EPS;
    j=NY-1
    A[i*NX+j][(i-1)*NX+j]-=1/(dX)**2;
    A[i*NX+j][i*NX+(j-1)]-=1/(dY)**2;
    A[i*NX+j][i*NX+j]-=-2/(dX)**2-2/(dY)**2;
    b[i*NX+j]-=-rho[i][j]/EPS;

    x=CG(A,x,b,Conv)

##テキストファイルに書き出し
    FILE = os.path.dirname(__file__)+"/SLE100.txt"
    f = open(FILE, 'w') # ファイルを開く(該当ファイルがなければ新規作成)
    f.write("x   y    phi(x,y)\n")
    for i in range(0,NX):
      for j in range(0,NY):
            f.write("{}   {}    {}\n".format(i*dX, j*dY, x[i*NX+j]))
    f.close() # ファイルを閉じる

if __name__ == "__main__":
    main()
    print("終了")
