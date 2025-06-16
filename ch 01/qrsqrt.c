#include <stdio.h>
#include <math.h>

float Q_rsqrt(float number) {
  long i;
  float x2, y;
  const float threehalfs = 1.5F;

  x2 = number * 0.5F;
  y  = number;
  i  = *(long*)&y;                            // evil floating point bit level hacking
  i  = 0x5f3759df - ( i >> 1 );               // what the fuck?
  y  = *(float*)&i;
  y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
  // y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

  return y;
}


int main() {
    float number = 1.0;

    while(number > 0) {
        printf("Enter a floating-point number: ");
        if (scanf("%f", &number) != 1) {
            fprintf(stderr, "Invalid input. Please enter a valid number.\n");
            return 1;
        }

        float result = Q_rsqrt(number);
        float exact = 1.0f / sqrtf(number);
        printf("The inverse square root of %f is approximately %f with relative error %f\n", 
            number, result, fabs(result-exact)/exact);
    }

    return 0;
}