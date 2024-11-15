from pathlib import Path
from time import sleep


def build_diagram(response):
    sleep(5)
    return str(Path(__file__).parent) + "/resources/icon.jpg"

def parse_database_structure(database):
    return """CREATE TABLE Branch (
            BranchID INT PRIMARY KEY
        );

        CREATE TABLE Headquarters (
            HeadquartersID INT PRIMARY KEY,
            BranchID INT,
            FOREIGN KEY (BranchID) REFERENCES Branch(BranchID)
        );

        CREATE TABLE Supplier (
            SupplierID INT PRIMARY KEY,
            DeliveryID INT,
            DeliveryDate DATE
        );

        CREATE TABLE Product (
            ProductID INT PRIMARY KEY,
            SupplierID INT,
            FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
        );

        CREATE TABLE Delivery (
            DeliveryID INT PRIMARY KEY,
            DeliveryDate DATE,
            SupplierID INT,
            FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
        );

        CREATE TABLE `Order` (
            OrderID INT PRIMARY KEY,
            OrderDate DATE,
            HeadquartersID INT,
            FOREIGN KEY (HeadquartersID) REFERENCES Headquarters(HeadquartersID)
        );

        CREATE TABLE OrderDetail (
            OrderDetailID INT PRIMARY KEY,
            ProductID INT,
            OrderID INT,
            ProductQuantity INT,
            FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
            FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
        );

        CREATE TABLE OrderDetailDelivery (
            DeliveryID INT,
            OrderID INT,
            OrderDetailID INT,
            PRIMARY KEY (DeliveryID, OrderID, OrderDetailID),
            FOREIGN KEY (DeliveryID) REFERENCES Delivery(DeliveryID),
            FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID),
            FOREIGN KEY (OrderDetailID) REFERENCES OrderDetail(OrderDetailID)
        );
        """

def build_payload(prompt):
    return {
        "query": "INSERT INTO `Branch` (`BranchId`) VALUES ('2706');"
    }
