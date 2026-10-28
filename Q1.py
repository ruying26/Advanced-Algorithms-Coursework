import time

# Hash Function
def hash_numeric(key, table_size):
    # Division method
    return key % table_size

# Entity Class
class Product:

    def __init__(self, product_id, name, price, quantity):

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def display(self):

        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Price: RM{self.price:.2f} | "
            f"Stock: {self.quantity}"
        )

# Hash Table
# Open Addressing + Linear Probing
class PharmacyHashTable:
    def __init__(self, size):

        self.size = size

        # Slot / Bucket structure
        self.keys = [None] * size
        self.values = [None] * size

    # Insert with collision explanation
    def insert(self, key, value, show_message=True):

        index = hash_numeric(
            key,
            self.size
        )

        start = index
        probes = 0

        if show_message:
            print("\n========== INSERT PROCESS ==========")
            print("Hash calculation:")
            print(f"{key} % {self.size} = {index}")
            print(f"Initial slot: {index}")

        while self.keys[index] is not None:
            # Duplicate checking
            if self.keys[index] == key:
                print("Product ID already exists!")
                return False

            if show_message:
                print("\nCollision detected!")
                print(f"Slot {index} is occupied by:")
                print(self.values[index].display())

            probes += 1
            old_index = index

            # Linear Probing
            index = (index + 1) % self.size

            if show_message:
                print("\nLinear Probing calculation:")

                print(f"({old_index} + 1) % {self.size} = {index}")

            if index == start:
                raise Exception("Hash Table Full")

        self.keys[index] = key

        self.values[index] = value

        if show_message:
            print("\nProduct inserted successfully!")
            print(f"Final slot: {index}")
            print(f"Total probes: {probes}")

        return True

    # Search
    def search(self, key):
        index = hash_numeric(
            key,
            self.size
        )
        start = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]

            index = (index + 1) % self.size

            if index == start:
                break

        return None

    # Display Hash Table
    def display(self):
        print("\n========== HASH TABLE ==========")

        for i in range(self.size):
            if self.keys[i] is None:
                print(f"Slot [{i}] : Empty")

            else:
                print(
                    f"Slot [{i}] : "
                    f"{self.values[i].display()}"
                )


# Array Search for Performance Comparison
def array_search(array, product_id):
    for product in array:
        if product.product_id == product_id:
            return product

    return None


# Pharmacy Inventory System
class PharmacyInventorySystem:

    def __init__(self, table_size):
        self.hash_table = PharmacyHashTable(table_size)

        # 1D Array storage
        self.products = []

    # Insert Product
    def insert_product(self, product):

        result = self.hash_table.insert(
            product.product_id,
            product,
            show_message=True
        )

        if result:
            self.products.append(product)

    # Search Product + Performance Comparison
    def search_product(self, product_id):

        print("\n========== SEARCH ==========")

        # Hash Table Searching
        start = time.perf_counter()

        hash_result = self.hash_table.search(product_id)

        end = time.perf_counter()

        hash_time = end - start

        # Array Searching
        start = time.perf_counter()
        array_result = array_search(
            self.products,
            product_id
        )

        end = time.perf_counter()

        array_time = end - start

        # Display Product Result
        if hash_result:
            print("Product Found:")
            print(hash_result.display())

        else:
            print("Product Not Found")

        # Display Performance
        print("\nSearching Performance:")
        print(
            f"Hash Table Search: "
            f"{hash_time:.8f} seconds"
        )

        print(
            f"Array Search: "
            f"{array_time:.8f} seconds"
        )

        if hash_time < array_time:
            print("Hash Table search is faster.")

        else:
            print("Array search is faster.")

    # Display Hash Table
    def display(self):
        self.hash_table.display()

# Main Program
def main():

    # Hash Table size = 17 (for collision demonstration)
    system = PharmacyInventorySystem(17)

    # Predefined Pharmacy Records
    products = [

        Product(
            1042,
            "Paracetamol 500mg",
            5.90,
            120
        ),

        Product(
            2055,
            "Vitamin C",
            12.50,
            80
        ),

        Product(
            3090,
            "Cough Syrup",
            8.90,
            60
        ),

        Product(
            4015,
            "Antibiotic",
            25.00,
            40
        )

    ]


    # Load predefined records
    print("Loading pharmacy records...")


    for product in products:

        system.hash_table.insert(
            product.product_id,
            product,
            show_message=False
        )

        # Store same data in 1D array
        system.products.append(product)


    print(
        f"{len(products)} product records loaded successfully."
    )


    # Menu
    while True:

        print("\n================================")
        print(" Pharmacy Inventory System ")
        print("================================")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Display Hash Table")
        print("4. Exit")


        choice = input("Enter choice: ")


        if choice == "1":

            try:

                product_id = int(input("Enter Product ID: "))
                name = input("Enter Product Name: ")
                price = float(input("Enter Price: "))
                quantity = int(input("Enter Quantity: "))


                if product_id <= 0:
                    print("Product ID must be positive!")
                    continue


                if price < 0 or quantity < 0:
                    print("Price and quantity cannot be negative!")
                    continue


                product = Product(
                    product_id,
                    name,
                    price,
                    quantity
                )


                system.insert_product(product)


            except ValueError:

                print("Invalid input!")


        elif choice == "2":

            try:

                product_id = int(input("Enter Product ID: "))

                system.search_product(product_id)


            except ValueError:

                print("Invalid Product ID!")


        elif choice == "3":

            system.display()


        elif choice == "4":

            print("System terminated.")
            break


        else:

            print("Invalid choice.")

# Run Program
if __name__ == "__main__":
    main()