import ghasedakpack as ghasedak


def send_register_sms(receptor, sms_code):
    sms = ghasedak.Ghasedak("1ee7c989c050f0c5b0aaee30b88fbc95b349f4e04aa959419d0ddac54c69588f")

    sms_verification = sms.verification(
        {'receptor': receptor, 'type': '1', 'template': 'RegisterSMSCode', 'param1': sms_code})

    return sms_verification


def send_forget_password_sms(receptor, sms_code):
    sms = ghasedak.Ghasedak("1ee7c989c050f0c5b0aaee30b88fbc95b349f4e04aa959419d0ddac54c69588f")

    sms_verification = sms.verification(
        {'receptor': receptor, 'type': '1', 'template': 'ForgetPasswordSMSCode', 'param1': sms_code})

    return sms_verification


def send_delete_account_sms(receptor, sms_code):
    sms = ghasedak.Ghasedak("1ee7c989c050f0c5b0aaee30b88fbc95b349f4e04aa959419d0ddac54c69588f")

    sms_verification = sms.verification(
        {'receptor': receptor, 'type': '1', 'template': 'DeleteAccountSMSCode', 'param1': sms_code})

    return sms_verification


def send_admin_order_complete_sms(receptor, customer, order_price):
    sms = ghasedak.Ghasedak("1ee7c989c050f0c5b0aaee30b88fbc95b349f4e04aa959419d0ddac54c69588f")

    sms_verification = sms.verification(
        {'receptor': receptor, 'type': '1', 'template': 'AdminOrderComplete', 'param1': customer,
         'param2': order_price})

    return sms_verification


def send_customer_order_complete_sms(receptor, order_price):
    sms = ghasedak.Ghasedak("1ee7c989c050f0c5b0aaee30b88fbc95b349f4e04aa959419d0ddac54c69588f")

    sms_verification = sms.verification(
        {'receptor': receptor, 'type': '1', 'template': 'CustomerOrderComplete', 'param1': order_price})

    return sms_verification


def send_product_in_stock_reached_danger_zone(receptor, product_barcode, product_name, danger_zone):
    sms = ghasedak.Ghasedak("1ee7c989c050f0c5b0aaee30b88fbc95b349f4e04aa959419d0ddac54c69588f")

    sms_verification = sms.verification(
        {'receptor': receptor, 'type': '1', 'template': 'ProductInStockReachedDangerZone', 'param1': danger_zone,
         'param2': product_name, 'param3': product_barcode})

    return sms_verification
