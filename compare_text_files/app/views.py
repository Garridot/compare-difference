
from django.contrib import messages
from django.shortcuts import redirect, render
import pdfplumber
import docx2txt



def main(request):
    context = {}
    changed_ = []
    if request.method == 'POST':
        
        # if request.POST['original'] == '' or request.POST['changed'] == '' :
        #     messages.error(request, 'Oops, Both text fields are required.')
        #     return redirect('main')

        if request.POST['original'] and request.POST['changed']:
            first  = request.POST['original']
            second   = request.POST['changed']

            for f,s in zip(first.split('\n'),second.split('\n')):    
                if f == s:   changed_.append(f"""<html><span>{s}</span></html>""")
                elif f != s: changed_.append(f"""<html><span class='changed'>{s}</span></html>""") 



        elif request.FILES['original_'] and request.FILES['changed_']:

            if request.FILES['original_'] == '' or request.FILES['changed_'] == '' :
                messages.error(request, 'Oops, Both files are required.')
                return redirect('main') 

            else:
                original  = request.FILES['original_']
                changed   = request.FILES['changed_']

                o_ext,c_ext = str(original).split('.')[-1].lower() , str(changed).split('.')[-1].lower()

                try:
                    with pdfplumber.open(original) as pdf: first = str(pdf.pages[0].extract_text())
                except: 
                    first  = docx2txt.process(original)

                try:
                    with pdfplumber.open(changed) as pdf:  second = str(pdf.pages[0].extract_text()) 
                except: 
                    second = docx2txt.process(changed)      
                
                    
                for f,s in zip(first.split('\n'),second.split('\n')):    
                    if f == s:   changed_.append(f"""<html><span>{s}</span></html>""")
                    elif f != s: changed_.append(f"""<html><span class='changed'>{s}</span></html>""") 
       
        
        try:    context['original'] = [f for f in first.split('\n')] 
        except: context['original'] = [f for f in first]
        context['changed']  = [c for c in changed_]
        

    return render(request,'main.html',context)


