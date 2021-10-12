//
// Created by Hariharan Ragothaman on 10/12/21.
//

#include "bits/stdc++.h"
using namespace std;

//Abstract Factory is a creational design pattern that lets you produce families of related objects without specifying their concrete classes

/*
 *  Each distinct product of a product family should have a base interface
 *  All variants of the product must implement the interface
 */

class AbstractProductA {
public:
    virtual ~AbstractProductA() {};
    virtual string UsefulFunctionA() const = 0;
};

class ConcreteProductA1: public AbstractProductA {
public:
    string UsefulFunction() const override {
        return "The result of Product-A1";
    }
};

class ConcreteProductA2: public AbstractProductA {
    string UsefulFunction() const override {
        return "The result of Product-A2";
    }
};

/* End of Abstract Product A */

/* Now let's interface another product */

class AbstractProductB
{
public:
    virtual ~AbstractProductB() {};
    virtual string UsefulFunctionB() const = 0;
};



