#include <math.h> 
#include <stdio.h>
#include <stdlib.h>

#define N 100 //ドット数

int main(void){//すべてSI単位系

 const double delta=1.0/(N-1); //刻み幅[m] //1はint型だから割り算は切り捨て、1.0はdouble型
 const double center=(N-1)/2.0;
 double phi[N][N]; //電位[V]
 double rho[N][N]; //電荷密度[C/m^2]
 int metal[N][N]; //導体が存在:1,不存在;0
 const double eps=8.85e-12; //真空の誘電率[F/m]
 double MaxPhi=1e-10;
 double Prev_phi;
 double CurErr;
 double MaxErr;
 const double Conv=1e-6;
 int loop=0;
 int i,j;
 
 
 //初期化
 for(i=0;i<N;){
  for(j=0;j<N;){
   phi[i][j]=0; //電位の初期化
   
   if(delta*delta*(pow((i-center),2)+pow((j-center),2))<=0.05*0.05){
    rho[i][j]=1e-8; //電荷を置く
   }else{rho[i][j]=0;}
   
   if(delta*delta*(pow((i-0.3*N),2)+pow((j-0.3*N),2))<=0.10*0.10){
    metal[i][j]=1;//導体を置く
   }else{metal[i][j]=0;}
   j=j+1;
  }
  i=i+1;
 }
 
 do{
   MaxErr=CurErr=0;
   for(i=1;i<N-1;i=i+1){
     for(j=1;j<N-1;j=j+1){
     if(metal[i][j]==0){
       Prev_phi=phi[i][j];
       phi[i][j]=0.25*(pow(delta,2)*rho[i][j]/eps+phi[i+1][j]+phi[i-1][j]+phi[i][j+1]+phi[i][j-1]);
       if(MaxPhi<fabs(phi[i][j])){
         MaxPhi=phi[i][j];
        }
       CurErr=(fabs(phi[i][j]-Prev_phi))/MaxPhi; //前回ループからの変動
       if(CurErr>MaxErr){
         MaxErr=CurErr; //前回ル―プからの系内最大変動
         }
        }
       }
     }
    printf("ループ%d回目 %e\n",loop, MaxErr);
    loop=loop+1;
  }while(MaxErr>Conv);


 FILE *fp;
 fp=fopen("2DPoisson_電荷密度.txt","w");
 fprintf(fp,"x\ty\trho[x][y]\n");
 for(j=0;j<N;j=j+1){
   for(i=0;i<N;i=i+1){
     fprintf(fp, "%f\t%f\t%e\n", i*delta, j*delta, rho[i][j]);
    }
  }
 fclose(fp);
 printf("電荷密度ファイル出力完了\n");


 fp=fopen("2DPoisson_電位.txt","w");
 fprintf(fp,"x\ty\tphi[x][y]\n");
 for(j=0;j<N;j=j+1){
   for(i=0;i<N;i=i+1){
     fprintf(fp, "%f\t%f\t%e\n", i*delta, j*delta, phi[i][j]);
    }
  }
 fclose(fp);
 printf("電位ファイル出力完了\n");
 
 
}
