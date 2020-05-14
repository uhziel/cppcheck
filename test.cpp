class A { public: int i; int* GetValue() {return &i;} };
A GetA() { return A(); }
void func(int* p) { (*p) += 1; }
int main1()
{
   int* v = GetA().GetValue();
   func(v);
   //func(GetA().GetValue());
   //func(A().GetValue());
   return 0;
}
