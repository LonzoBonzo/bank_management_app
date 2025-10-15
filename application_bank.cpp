#include "bank.h"
#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;

Bank::Bank(string file_name) {
    num_client = 0;
    clients = nullptr;
    load_clients_info(file_name);
}

Bank::Bank(const Bank& other) {
    num_client = other.num_client;
    clients = new Client[num_client]; 
    for (int i - 0; i < num_clients; i++) {
        clients[i] = other.clients[i];
    }

}

Bank::~Bank() {
    delete[] clients; 
}

void Bank::load_clients_info(string file_name) {
    ifstream input_file(file_name); 
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

string Bank::withdraw(double account_number, double amount) {
    for (int i = 0; i < num_clients; i++) {
        if (clients[i],bank_account_number == account_number) {
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

void Bank::saving_info(string file_name) {
    ofstream fout(file_name);
    fout << num_client << endl;
    for (int = 0; i < num_client; i++) {
        fout << clients[i].client_name << " " << clients[i].ssn
    }
    fout.close();
}

void Bank::find_client(double account_number) {
    for (int i = 0; i < num_client; i++) {
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

void Bank::add_new_client(Client new_client) {
    Client* temp = new Client[num_client + 1];
    for (int i = 0; i < num_client; i++) {
        temp[i] = clients[i];
    }
    temp[num_client] = new_client;
    delete[] clients;
    clients = temp;
    num_client++;
}
