import json

def plager(uploaded_token, pdf_p_name):
    
    with open('./static/json/data.json', "r") as v:
        datat = json.load(v)
        
    with open('./static/json/pdf_name.json', "r") as d:
        datat_name = json.load(d)
        
    with open('./static/json/plager.json', "r") as x:
        plagered = json.load(x)
        
    datat_length = len(datat)
    
    # plagered[pdf_p_name] = None
    
    # plagered.append({
    #     pdf_p_name : ""
    # })
    
    # count = 0
    plagered_times_data = []
    
    trigrams_p=[]

    for c in range(len(uploaded_token)-2):
        t=(uploaded_token[c],uploaded_token[c+1],uploaded_token[c+2])
        trigrams_p.append(t)
    
    
    count = 0
    
    for j in range(1, datat_length-1):
        s=0
        trigrams_o=[]
        
        # print(j)
        l = str(j)
        
        # print(datat[l])
        
        for i in range(len(datat[l])-2):
            p = (datat[l][i],datat[l][i+1],datat[l][i+2])
            trigrams_o.append(p)
            if p in trigrams_p:
                s+=1
        
        C=s/len(trigrams_o)
        
        if ( C >= 0.60) :
           count += 1 
           plagered_times_data.append(datat_name[l] + " " + str(C*100) + "%")
           
       
    if(count == 0):
        plagered_times_data.append("Not Plagiarised")
        
                
    plagered[pdf_p_name] = plagered_times_data
    
    with open('./static/json/plager.json', 'w') as r:
        json.dump(plagered, r)
            