#include "bank.h"
#include <iostream>
using namespace std;

int main() {
    Bank myBank ("clients.txt");

    myBank.find_client(1001); 
    myBank.deposit(1001, 500);
    myBank.withdraw(1002, 100);

    Client newClient = {"Charlie", "589-340-6628", 1004, 750};
    myBank.add_new_client(newClient);
    myBank.saving_info("clients.txt");

    return 0;
}