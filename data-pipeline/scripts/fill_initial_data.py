from gen_helper.db import connect_to_mongo, close_mongo_connection, write_bill_to_mongo


def main(client):

    # Alectra
    alectra_billing_info = [0, 98.29, 106.79, 116.75, 96.77, 152.08, 205.23, 209.31, 236.21]

    # Brampton Water
    bw_billing_info = [0, 0, 0, 180.71, 0, 0, 363.03, 0, 0]

    # Enbridge
    enbridge_billing_info = [0, 207.98, 175.4, 167.05, 207.19, 107.18, 51.94, 72.82, 57.59]

    # # Reliance Water Heater
    reliance_billing_info = [0, 39.08, 39.08, 39.72, 40.44, 40.44, 40.44, 40.44, 40.44]

    for i in range(1, 9):
        write_bill_to_mongo(client, "Reliance Water Heater", reliance_billing_info[i], i, 2024)
        write_bill_to_mongo(client, "Enbridge", enbridge_billing_info[i], i, 2024)
        write_bill_to_mongo(client, "Brampton Water", bw_billing_info[i], i, 2024)
        write_bill_to_mongo(client, "Alectra", alectra_billing_info[i], i, 2024)


if __name__ == "__main__":
    client = connect_to_mongo()
    main(client)
    close_mongo_connection(client)
