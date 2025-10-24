#include "bank.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
using namespace std;

//Constructor..

Bank::Bank(string file_name) {
    num_clients = 0;
    clients = nullptr;
    load_clients_info(file_name);
}

//Deep Constructor.

Bank::Bank(const Bank& other) {
    num_clients = other.num_clients;
    clients = new Client[num_clients]; 
    for (int i = 0; i < num_clients; i++) {
        clients[i] = other.clients[i];
    }

}

//Destructor..
Bank::~Bank() {
    delete[] clients; 
}

void Bank::load_clients_info(string file_name) {
    ifstream fin(file_name); 
    if(!fin) {
        cout << "Error opening file: " << file_name << endl;
        return;
    }


    fin >> num_clients; 
    clients = new Client[num_clients];

    for (int i = 0; i < num_clients; i++) {
        fin >> clients[i].client_name >> clients[i].ssn >> clients[i].bank_account_number >> clients[i].balance;
    }
    fin.close();
}

Client* Bank::get_clients_info() {
    return clients;
}

//This is the deposity btw.

double Bank::deposit(double account_number, double amount) {
    for (int i = 0; i < num_clients; i++) {
        if (clients[i].bank_account_number == account_number) {
            clients[i].balance += amount;
            return clients[i].balance;
        }
    }
    cout << "Account number not found. \n" << endl;
    return -1;
}

//The withdrawl feature. REMEMEBER IT PLEASE.

string Bank::withdraw(double account_number, double amount) {
    for (int i = 0; i < num_clients; i++) {
        if (clients[i].bank_account_number == account_number) {
            if (clients[i].balance >= amount) {
                clients [i].balance -= amount;
                return "Withdrawal Updated. \n";
            } else {
                return "Not enough balance to withdraw. \n";
            }
        }
    }
    return "Account number not found. \n";
}

// Info saving section.

void Bank::saving_info(string file_name) {
    ofstream fout(file_name);
    fout << num_clients << endl;
    for (int i = 0; i < num_clients; i++) {
        fout << clients[i].client_name << " " 
        << clients[i].ssn << " " 
        << clients[i].bank_account_number << " " 
        << clients[i].balance << endl;
    }
    fout.close();
}


// Finding client section.
void Bank::find_client(double account_number) {
    for (int i = 0; i < num_clients; i++) {
        if (clients[i].bank_account_number == account_number) {
            cout << "Client's Name: " << clients[i].client_name << endl;
            cout << "SSN: " << clients[i].ssn << endl;
            cout << "Account Number: " << clients[i].bank_account_number << endl;
            cout << "Balance: $" << fixed << setprecision(2) << clients[i].balance << endl;
            return;
        }
    }
    cout << "This person doesn't exist. \n" << endl;
}

//ADDING a new client section.

void Bank::add_new_client(Client new_client) {
    Client* temp = new Client[num_clients + 1];
    for (int i = 0; i < num_clients; i++) {
        temp[i] = clients[i];
    }
    temp[num_clients] = new_client;
    delete[] clients;
    clients = temp;
    num_clients++;
}

extern "C" {
    Bank* Bank_new(const char* file_name) {return new Bank(file_name);}
    void Bank_delete(Bank* b) {delete b;}
    double Bank_deposit(Bank* b, double acc, double amount) {return b->deposit(acc, amount);}

    const char* Bank_withdraw(Bank* b, double acc, double amount) {
        static std::string result;
        result = b->withdraw(acc, amount);
        return result.c_str();
    }
    void Bank_find_client(Bank* b, double acc) {b->find_client(acc);}
    void Bank_add_new_client(Bank* b, const char* name, const char* ssn, double acc, double bal) {
        Client c = {name, ssn, acc, bal};
        b->add_new_client(c);
    }
    void Bank_save(Bank* b, const char* file_name) {b->saving_info(file_name);}

    const char* Bank_get_client_name(Bank* b, double acc) {
        static std::string name;
        for (int i = 0; i < b->num_clients; i++) {
            if (b->clients[i].bank_account_number == acc) {
                name = b->clients[i].client_name;
                return name.c_str();
            }
        }
        return nullptr;
    }

    const char* Bank_get_client_phone(Bank* b, double acc) {
        static std::string phone;
        for (int i = 0; i < b->num_clients; i++) {
            if (b->clients[i].bank_account_number == acc) {
                phone = b->clients[i].ssn;
                return phone.c_str();
            }
        }
        return nullptr;
    }

    const char* Bank_get_client_ssn(Bank* b, double acc) {
        static std::string tmp;
        for (int i = 0; i < b->num_clients; i++) {
            if (b->clients[i].bank_account_number == acc) {
                tmp = b->clients[i].ssn;
                return tmp.c_str();
            }
        }
        return nullptr;
    }

    double Bank_get_client_balance(Bank* b, double acc) {
        for (int i =0; i < b->num_clients; i++) {
            if (b->clients[i].bank_account_number == acc) {
                return b->clients[i].balance;
            }
        }
        return -1;
    }
}
