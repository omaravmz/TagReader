from functions import read_image, extract_brand, extract_model, extract_serial, save_product

brand_names = ["APPLE", "HUAWEI", "DELL", "HP", "ASUS", "SAMSUNG"]
archivo = "products.csv"

#EJEMPLO HUAWEI
product_name = read_image("public/huawei.jpg")
brand = extract_brand(product_name, brand_names)
model = extract_model(product_name)
serial = extract_serial(product_name)

save_product(brand, model, serial, archivo)

#EJEMPLO HP
product_name = read_image("public/hp.jpg")
brand = extract_brand(product_name, brand_names)
model = extract_model(product_name)
serial = extract_serial(product_name)

save_product(brand, model, serial, archivo)

#EJEMPLO SAMSUNG
product_name = read_image("public/samsung.jpg")
brand = extract_brand(product_name, brand_names)
model = extract_model(product_name)
serial = extract_serial(product_name)

save_product(brand, model, serial, archivo)