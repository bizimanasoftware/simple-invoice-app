from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import RegistrationForm, LoginForm, ProductForm
from .models import Product, Receipt, ReceiptItem, Client
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.http import HttpResponse

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['pin'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('menu:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'menu/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pin = form.cleaned_data['pin']
            user = authenticate(request, username=username, password=pin)
            if user is not None:
                login(request, user)
                return redirect('menu:dashboard')
            else:
                form.add_error(None, "Invalid username or PIN.")
    else:
        form = LoginForm()
    return render(request, 'menu/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('menu:login')

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('menu:dashboard')
    else:
        product_form = ProductForm()

    products = Product.objects.filter(user=request.user)
    return render(request, 'menu/dashboard.html', {
        'product_form': product_form,
        'products': products
    })

@login_required
def delete_product_view(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id, user=request.user)
            product.delete()
        except Product.DoesNotExist:
            pass
    return redirect('menu:dashboard')

@login_required
def get_products_for_receipt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_ids = data.get('product_ids', [])
            products = Product.objects.filter(id__in=product_ids, user=request.user).values()
            return JsonResponse(list(products), safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({}, status=400)

@login_required
def generate_receipt_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            client_name = data.get('client_name', '')
            seller_name = data.get('seller_name', 'My Business')

            client = None
            if client_name:
                client, _ = Client.objects.get_or_create(user=request.user, name=client_name)

            receipt = Receipt.objects.create(
                user=request.user,
                client=client,
                seller_name=seller_name
            )

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="receipt_{receipt.id}.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            story = []
            
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='ReceiptTitle', fontSize=24, leading=28, alignment=1, spaceAfter=20))
            styles.add(ParagraphStyle(name='Header', fontSize=14, leading=16, alignment=1, spaceAfter=6))
            styles.add(ParagraphStyle(name='ReceiptBodyText', fontSize=10, leading=12, spaceBefore=6))

            story.append(Paragraph("Receipt", styles['ReceiptTitle']))
            story.append(Paragraph(f"Date: {receipt.created_at.strftime('%B %d, %Y')}", styles['Header']))
            story.append(Paragraph(f"Time: {receipt.created_at.strftime('%I:%M %p')}", styles['Header']))
            story.append(Spacer(1, 0.25*inch))
            
            story.append(Paragraph(f"<b>Seller:</b> {seller_name}", styles['ReceiptBodyText']))
            if client:
                story.append(Paragraph(f"<b>Client:</b> {client.name}", styles['ReceiptBodyText']))
            story.append(Spacer(1, 0.25*inch))
            
            data = [['Product', 'Qty', 'Price', 'Discount %', 'Tax %', 'Total']]
            subtotal = 0
            total_discount = 0
            total_tax = 0

            for item in items:
                price = float(item.get('price', 0))
                quantity = int(item.get('quantity', 0))
                discount_percent = float(item.get('discount', 0))
                tax_percent = float(item.get('tax', 0))

                ReceiptItem.objects.create(
                    receipt=receipt,
                    product_name=item.get('name', 'N/A'),
                    quantity=quantity,
                    price=price,
                    discount_percent=discount_percent,
                    tax_percent=tax_percent
                )
                
                item_subtotal = price * quantity
                discount_amount = item_subtotal * (discount_percent / 100)
                price_after_discount = item_subtotal - discount_amount
                tax_amount = price_after_discount * (tax_percent / 100)
                item_total = price_after_discount + tax_amount
                
                subtotal += item_subtotal
                total_discount += discount_amount
                total_tax += tax_amount
                
                data.append([
                    item.get('name', 'N/A'),
                    str(quantity),
                    f"${price:.2f}",
                    f"{discount_percent:.2f}%",
                    f"{tax_percent:.2f}%",
                    f"${item_total:.2f}"
                ])

            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ])
            
            table = Table(data, colWidths=[2*inch, 0.5*inch, 0.75*inch, 1*inch, 0.75*inch, 1*inch])
            table.setStyle(table_style)
            story.append(table)
            
            story.append(Spacer(1, 0.25*inch))
            
            final_total = subtotal - total_discount + total_tax
            story.append(Paragraph(f"<b>Subtotal:</b> ${subtotal:.2f}", styles['ReceiptBodyText']))
            story.append(Paragraph(f"<b>Discount:</b> -${total_discount:.2f}", styles['ReceiptBodyText']))
            story.append(Paragraph(f"<b>Tax:</b> +${total_tax:.2f}", styles['ReceiptBodyText']))
            story.append(Paragraph(f"<b><font size=14>TOTAL: ${final_total:.2f}</font></b>", styles['ReceiptBodyText']))

            doc.build(story)
            return response

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            return JsonResponse({'error': f'Invalid data in request: {e}'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)