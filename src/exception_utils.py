def get_text(element):
    try:
        return element.get_text()
    except Exception:
        return None

def get_len(mylist):
    try:
        return len(mylist)
    except Exception:
        return None

def get_href(element):
    try:
        return element['href']
    except Exception:
        return None

def get_value_by_idx_list(mylist, idx):
    try:
        return mylist[idx]
    except Exception:
        return None

def get_a_children_by_find(element, children_name):
    try:
        return element.find(children_name)
    except Exception:
        return None

def get_a_children_by_find_class(element, children_name, class_name):
    try:
        return element.find(children_name, class_=class_name)
    except Exception:
        return None



def get_childrens_by_find(element, children_name):
    try:
        return element.find_all(children_name)
    except Exception:
        return None
    
def get_childrens_by_find_no_recursive(element, children_name):
    try:
        return element.find_all(children_name, recursive=False)

    except Exception:
        return None

def get_childrens_by_find_class(element, children_name, class_name):
    try:
        return element.find_all(children_name, class_= class_name)
    except Exception:
        return None