#include<cstdlib>
#include<cstdio>
#include<cmath>
using namespace std;

typedef struct Ball
{
    double x;
    double y;
    double r;
}ball;

typedef struct ballList
{
    struct ballList * next;
    Ball ball;
}BallList;

void insert(Ball ball);
double distance(Ball b1, Ball b2);
int judge(Ball b);
void putBall();
void putPoint(double x, double y);
double abs_(double num);

BallList *head = NULL;
double step = 0.01;
int num = 0;
double sumr = 0;

int main(){
	freopen("test.txt","w",stdout);
    int n, pointNum, i;
    printf("The number of balloon(s): ");
    scanf("%d",&n);
    printf("The number of point(s)");
    scanf("%d",&pointNum);
    for(i = 0; i < pointNum; i ++){
        printf("The %d th point's position(x y)£º",i+1);
        double x, y;
        scanf("%lf %lf", &x, &y);
        putPoint(x, y);
    }
    printf("\nBalloon No\t x-coordinate\t y-coordinate\t radius\t r^2 sum\n");
    for(i = 0; i < n; i ++){
        putBall();
    }
    printf("\nr^2sum:\t %lf\n", sumr);
    return 0;
}

void putPoint(double x, double y){
    Ball ball = {x, y, 0};
    insert(ball);
}

void insert(Ball ball){
    ballList * newBall = (ballList *)malloc(sizeof(ballList));
    newBall->ball = ball;
    newBall->next = head;
    head = newBall;
}

void putBall()
{
    Ball ball = {-1 + step, -1 + step, 0};
    Ball maxBall = ball;
    int i, j;
    for (i = 0; ball.x < 1; ++i){
        ball.x += step;
        ball.y = -1 + step;
        for (j = 0; ball.y < 1; ++j){
            ball.y += step;
            ball.r = 0;
            double rstep = 0.1;
            while(rstep > 0.00001){
                if(ball.r > maxBall.r){
                    maxBall = ball;
                }
                ball.r += rstep;
                if(!judge(ball))
                {
                    ball.r -= rstep;
                    rstep /= 10;
                }
            }
        }
    }
    if(judge(maxBall)){
        insert(maxBall);
        num++;
        sumr += maxBall.r * maxBall.r;
        printf("%d\t %.3lf\t %.3lf\t %.3lf\t %lf \n", num, maxBall.x, maxBall.y, maxBall.r, sumr);
    }
}

int judge(Ball b)
{
    if((abs_(b.x) + b.r) > 1 || (abs_(b.y) + b.r) > 1)
    {
        return false;
    }
    ballList *tmp = head;
    while(tmp)
    {
        Ball ball = tmp->ball;
        if(distance(b, ball) < b.r + ball.r )
        {
            return false;
        }
        tmp = tmp->next;
    }
    return true;
}

double abs_(double num)
{
    if(num > 0)
        return num;
    return 0 - num;
}

double distance(Ball b1, Ball b2)
{
    double x1 = b1.x;
    double y1 = b1.y;
    double x2 = b2.x;
    double y2 = b2.y;
    return pow((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2), 0.5);
}
