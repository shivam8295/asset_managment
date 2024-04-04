from orders.models import OrderDetail
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import socket
from asset_master.models import *
from django.forms.models import model_to_dict




class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.now().date()
        one_day_before = now + datetime.timedelta(days=1)
        two_day_before = now + datetime.timedelta(days=2)
        three_day_before = now + datetime.timedelta(days=3)

        orders_three_day_before = OrderDetail.objects.filter(return_date=three_day_before, order_dispatch= True)

        orders_due_two_day_before = OrderDetail.objects.filter(return_date=two_day_before, order_dispatch= True)

        orders_due_one_day_before = OrderDetail.objects.filter(return_date=one_day_before, order_dispatch= True)
        
        


        #Asset return reminder after end of return date...
        one_day_after = now - datetime.timedelta(days=1)
        two_day_after = now - datetime.timedelta(days=2)
        three_day_after = now - datetime.timedelta(days=3)

        orders_due_three_day_after = OrderDetail.objects.filter(return_date=three_day_after, order_dispatch= True)

        orders_due_two_day_after = OrderDetail.objects.filter(return_date=two_day_after, order_dispatch= True)

        orders_due_one_day_after = OrderDetail.objects.filter(return_date=one_day_after, order_dispatch= True)



        order_reminder_list_before = [orders_three_day_before, orders_due_two_day_before, orders_due_one_day_before]

        order_reminder_list_after = [orders_due_three_day_after, orders_due_two_day_after, orders_due_one_day_after]


        for orders_reminder in order_reminder_list_before:
            if orders_reminder is not None:
                for order_obj in orders_reminder:
                    subject = 'Asset availability reminder'
                    context = {
                        'prepared_by_name': order_obj.prepared_by_name,
                        'prepared_by_email': order_obj.prepared_by_email,
                        'poc_at_venue_name': order_obj.poc_at_venue_name,
                        'approver_email': order_obj.approver_email,
                        'prepared_by_name': order_obj.prepared_by_name,
                        'return_date': order_obj.return_date,
                        'order_id': order_obj.id,
                    }
                    html_message = render_to_string('asset_return_email.html', context)
                    plain_message = strip_tags(html_message)
                    
                    # Create the email message with both HTML and plain text content
                    email = EmailMultiAlternatives(subject, plain_message, 'raunakron4@gmail.com', [order_obj.prepared_by_email, order_obj.approver_email])
                    email.attach_alternative(html_message, "text/html")  # Set the HTML content type
                    
                    # Send the email
                    email.send()
        
        
        for orders_reminder in order_reminder_list_after:
            if orders_reminder is not None:
                for order_obj in orders_reminder:
                    get_asset_form_order = model_to_dict(order_obj)
                    all_asset_list = get_asset_form_order.get('assets')
                    all_asset_list_ids=[]
                    for m in all_asset_list:
                        all_asset_list_ids.append(m.id)

                    asset_master_inventory_list = list(AssetMasterInventory.objects.filter(asset_id__in=all_asset_list_ids).values('asset_transfer',
                                                                                                'move_to_inventory',
                                                                                                'asset_id__description',
                                                                                                'asset_id__serial_no'))    

                    subject = 'Asset availability reminder'
                    context = {
                        'prepared_by_name': order_obj.prepared_by_name,
                        'prepared_by_email': order_obj.prepared_by_email,
                        'poc_at_venue_name': order_obj.poc_at_venue_name,
                        'approver_email': order_obj.approver_email,
                        'prepared_by_name': order_obj.prepared_by_name,
                        'return_date': order_obj.return_date,
                        'order_id': order_obj.id,
                        'asset_master_inventory_list':asset_master_inventory_list,
                        
                    }
                    html_message = render_to_string('asset_email_after_date.html', context)
                    plain_message = strip_tags(html_message)
                    
                    # Create the email message with both HTML and plain text content
                    email = EmailMultiAlternatives(subject, plain_message, 'raunakron00@gmail.com', [order_obj.prepared_by_email, order_obj.approver_email])
                    email.attach_alternative(html_message, "text/html")  # Set the HTML content type
                    
                    # Send the email
                    email.send()

