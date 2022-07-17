#include <iostream>
#include <string>

int main() {
  std::string tapa = "calamares";
  std::string* pointer = &tapa;

  std::cout << "tapa      " << tapa << "\n";
  std::cout << "&tapa     " << &tapa << "\n";
  std::cout << "pointer   " << pointer << "\n";
  std::cout << "*pointer  " << *pointer << "\n\n";

  tapa = "albondigas";

  std::cout << "tapa      " << tapa << "\n";
  std::cout << "&tapa     " << &tapa << "\n";
  std::cout << "pointer   " << pointer << "\n";
  std::cout << "*pointer  " << *pointer << "\n\n";

  *pointer = "croquetas de jamón";

  std::cout << "tapa      " << tapa << "\n";
  std::cout << "&tapa     " << &tapa << "\n";
  std::cout << "pointer   " << pointer << "\n";
  std::cout << "*pointer  " << *pointer << "\n";

  return 0;
}
