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

