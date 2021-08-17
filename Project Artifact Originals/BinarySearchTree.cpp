//============================================================================
// Name        : BinarySearchTree.cpp
// Author      : Daniel Ostrin
// Version     : 1.0
// Date        : 2/14/2020
// Copyright   : Copyright © 2017 SNHU COCE
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <algorithm>
#include <climits>
#include <iostream>
#include <string>
#include <iostream>
#include <time.h>
#include "CSVparser.hpp"
#include "CSVparser.cpp"

using namespace std;

//============================================================================
// Global definitions visible to all methods and classes
//============================================================================
// forward declarations
double strToDouble(string str, char ch);

struct Bid {
    string bidId; // unique identifier
    string title;
    string fund;
    double amount;
    Bid() {
        amount = 0.0;
    }
};

struct Node {
    Bid current;
    Node* left;
    Node* right;

    Node(Bid bid) {
        current = bid;
        left = NULL;
        right = NULL;
    }

    ~Node() {
        if (left) {
            delete left;
        }
        if (right) {
            delete right;
        }
    }
};

void displayBid(Bid bid) {
    cout
        << bid.bidId
        << ": "
        << bid.title
        << " | "
        << bid.amount
        << " | "
        << bid.fund
        << endl;

    return;
}

//============================================================================
// Binary Search Tree class definition
//============================================================================

/**
 * Define a class containing data members and methods to
 * implement a binary search tree
 */
class BinarySearchTree {

private:
    Node* root;
    void inOrder(Node* node);
    void removeNode(Node* rootNode, string removeBidId);

public:
    BinarySearchTree();
    virtual ~BinarySearchTree();
    void InOrder();
    void Insert(Bid bid);
    void Remove(string bidId);
    Bid Search(string bidId);
};

/**
 * Default constructor
 */
BinarySearchTree::BinarySearchTree() {
    // initialize housekeeping variables
    root = NULL;
}

/**
 * Destructor
 */
BinarySearchTree::~BinarySearchTree() {
    // recurse from root deleting every node
    if (this->root) {
        delete root;
    }
}

/**
 * Traverse the tree in order
 */
void BinarySearchTree::InOrder() {
    this->inOrder(this->root);
}
/**
 * Insert a bid
 */
void BinarySearchTree::Insert(Bid inputBid) {
    // Implement inserting a bid into the tree
    Node* prevNode = NULL;
    Node* testNode = this->root;
    string direction = "Z";

    while (testNode) {
        cout << testNode->current.bidId;
        prevNode = testNode;
        if (inputBid.bidId < testNode->current.bidId) {
            direction = "L";
            testNode = testNode->left;
        }
        else {
            direction = "R";
            testNode = testNode->right;
        }
    }

    if (not prevNode) {
        this->root = new Node(inputBid);
    }
    else {
        if (direction == "L") {
            prevNode->left = new Node(inputBid);
        }
        else {
            prevNode->right = new Node(inputBid);
        }
    }
}

/**
 * Remove a bid
 */
void BinarySearchTree::Remove(string removeBidId) {
    // Implement removing a bid from the tree
    removeNode(this->root, removeBidId);
}

/**
 * Search for a bid
 */
Bid BinarySearchTree::Search(string searchBidId) {
    //  Implement searching the tree for a bid
    Bid bid;
    Node* testNode = this->root;

    while (testNode) {
        if (testNode->current.bidId == searchBidId) {
            bid = testNode->current;
            break;
        }
        if (searchBidId < testNode->current.bidId) {
            testNode = testNode->left;
        }
        else {
            testNode = testNode->right;
        }
    }
    return bid;
}

void BinarySearchTree::inOrder(Node* node) {
    if (node) {
        // Recursive call left
        inOrder(node->left);

        // If left is done display current
        displayBid(node->current);

        // Recursive call right
        inOrder(node->right);
    }
}

void BinarySearchTree::removeNode(Node* rootNode, string removeBidId) {
    Node* parentNode = NULL;
    Node* currentNode = rootNode;
    while (currentNode) {
        // If we found bid
        if (currentNode->current.bidId == removeBidId) {
            // if neither left or right exist
            if (not currentNode->left && not currentNode->right) {
                if (not parentNode) {
                    currentNode = NULL;
                }
                else if (parentNode->left == currentNode) {
                    parentNode->left = NULL;
                }
                else {
                    parentNode->right = NULL;
                }
            }
            // if only left exists
            else if (currentNode->left && not currentNode->right) {
                if (not parentNode) {
                    currentNode->current = currentNode->left->current;
                }
                else if (parentNode->left == currentNode) {
                    parentNode->left = currentNode->left;
                }
                else {
                    parentNode->right = currentNode->left;
                }
            }
            // if only right exists
            else if (currentNode->right) {
                if (not parentNode) {
                    currentNode->current = currentNode->right->current;
                }
                else if (parentNode->left == currentNode) {
                    parentNode->left = currentNode->right;
                }
                else {
                    parentNode->right = currentNode->right;
                }
            }
            // if both exist
            else {
                Node* successorNode = currentNode->right;
                while (successorNode->left) {
                    successorNode = successorNode->left;
                }
                currentNode = successorNode;
                removeNode(currentNode->right, successorNode->current.bidId);
            }
        }
        // If removeBidId is less than current its in left branch
        if (removeBidId < currentNode->current.bidId) {
            currentNode = currentNode->left;
        }
        // Else right branch
        else {
            currentNode = currentNode->right;
        }
    }
    return;
}

//============================================================================
// Static methods used for testing
//============================================================================

/**
 * Load a CSV file containing bids into a container
 *
 * @param csvPath the path to the CSV file to load
 * @return a container holding all the bids read
 */
void loadBids(string csvPath, BinarySearchTree* bst) {
    cout << "Loading CSV file " << csvPath << endl;

    // initialize the CSV Parser using the given path
    csv::Parser file = csv::Parser(csvPath);

    // read and display header row - optional
    vector<string> header = file.getHeader();
    for (auto const& c : header) {
        cout << c << " | ";
    }
    cout << "" << endl;

    try {
        // loop to read rows of a CSV file
        for (unsigned int i = 0; i < file.rowCount(); i++) {

            // Create a data structure and add to the collection of bids
            Bid bid;
            bid.bidId = file[i][1];
            bid.title = file[i][0];
            bid.fund = file[i][8];
            bid.amount = strToDouble(file[i][4], '$');

            //cout << "Item: " << bid.title << ", Fund: " << bid.fund << ", Amount: " << bid.amount << endl;

            // push this bid to the end
            bst->Insert(bid);
        }
    }
    catch (csv::Error& e) {
        std::cerr << e.what() << std::endl;
    }
}

/**
 * Simple C function to convert a string to a double
 * after stripping out unwanted char
 *
 * credit: http://stackoverflow.com/a/24875936
 *
 * @param ch The character to strip out
 */
double strToDouble(string str, char ch) {
    str.erase(remove(str.begin(), str.end(), ch), str.end());
    return atof(str.c_str());
}

/**
 * The one and only main() method
 */
int main(int argc, char* argv[]) {

    // process command line arguments
    string csvPath, bidKey;
    switch (argc) {
    case 2:
        csvPath = argv[1];
        bidKey = "98109";
        break;
    case 3:
        csvPath = argv[1];
        bidKey = argv[2];
        break;
    default:
        csvPath = "eBid_Monthly_Sales_Dec_2016.csv";
        bidKey = "98109";
    }

    // Define a timer variable
    clock_t ticks;

    // Define a binary search tree to hold all bids
    BinarySearchTree* bst = new BinarySearchTree();

    Bid bid;

    int choice = 0;
    while (choice != 9) {
        cout << "Menu:" << endl;
        cout << "  1. Load Bids" << endl;
        cout << "  2. Display All Bids" << endl;
        cout << "  3. Find Bid" << endl;
        cout << "  4. Remove Bid" << endl;
        cout << "  9. Exit" << endl;
        cout << "Enter choice: ";
        cin >> choice;

        switch (choice) {
        case 1:
            bst = new BinarySearchTree();

            // Initialize a timer variable before loading bids
            ticks = clock();

            // Complete the method call to load the bids
            loadBids(csvPath, bst);

            // cout << bst->Size() << " bids read" << endl;

            // Calculate elapsed time and display result
            ticks = clock() - ticks; // current clock ticks minus starting clock ticks
            cout << "time: " << ticks << " clock ticks" << endl;
            cout << "time: " << ticks * 1.0 / CLOCKS_PER_SEC << " seconds" << endl;
            break;

        case 2:
            bst->InOrder();
            break;

        case 3:
            ticks = clock();

            bid = bst->Search(bidKey);

            ticks = clock() - ticks; // current clock ticks minus starting clock ticks

            if (!bid.bidId.empty()) {
                displayBid(bid);
            }
            else {
                cout << "Bid Id " << bidKey << " not found." << endl;
            }

            cout << "time: " << ticks << " clock ticks" << endl;
            cout << "time: " << ticks * 1.0 / CLOCKS_PER_SEC << " seconds" << endl;

            break;

        case 4:
            bst->Remove(bidKey);
            break;
        }
    }

    cout << "Good bye." << endl;

    return 0;
}
