#include <iostream> 
#include <string> 

#ifndef BANK_H 
#define BANK_H 

using namespace std; 

struct Client {
    string client_name;
    string ssn;
    double bank_account_number;
    double balance;
};

class Bank {
    private:
        int num_clients;
        Client* clients;

    public:
        Bank(string file_name);
        Bank(const Bank& other);
        ~Bank();

        void load_clients_info(string file_name);
        Client* get_clients_info();
        double deposit(double account_number, double amount);
        string withdraw(double account_number, double amount);
        void saving_info(string file_name);
        void find_client(double account_number);
        void add_new_client(Client new_client);
};

#endif
