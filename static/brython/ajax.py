
from browser import document, ajax, timer, window

# URL Query String
qs = ''
# URL to work on
url = ''


def bind_register_link(ev=None):
    try:
        document['header_register'].unbind('click', register_link_click)
    except: pass
    try:
        document['header_register'].bind('click', register_link_click)
    except: pass


def bind_register_footer_link(ev=None):
    try:
        document['footer_signup'].unbind('click', register_link_click)
    except: pass
    try:
        document['footer_signup'].bind('click', register_link_click)
    except: pass


def bind_register_button(ev):
    try:
        document['register_btn'].unbind('click', register_button_click)
    except: pass
    try:
        document['register_btn'].bind('click', register_button_click)
    except: pass


def bind_post_review_button(ev=None):
    try:
        document['post_review'].unbind('click', review_button_click)
    except: pass
    try:
        document['post_review'].bind('click', review_button_click)
    except: pass


def bind_login_button(ev):
    try:
        document['login_btn'].unbind('click', login_button_click)
    except: pass
    try:
        document['login_btn'].bind('click', login_button_click)
    except: pass


def bind_logout_button(ev=None):
    try:
        document['logout'].unbind('click', logout_click)
    except: pass
    try:
        document['logout'].bind('click', logout_click)
    except: pass


def bind_single_product_link(ev, product):
    try:
        product.unbind('click', products_id_click)
    except: pass
    try:
        product.bind('click', products_id_click)
    except: pass


def bind_404_link(ev, link):
    try:
        link.unbind('click', link_404_click)
    except: pass
    try:
        link.bind('click', link_404_click)
    except: pass


def bind_500_link(ev, link):
    try:
        link.unbind('click', link_500_click)
    except: pass
    try:
        link.bind('click', link_500_click)
    except: pass


def bind_my_acc_button(ev):
    try:

        for element in document.get(selector="li[id*='myacc_'"):
            element.unbind('click', account_click)
    except: pass
    try:
        for element in document.get(selector="li[id*='myacc_'"):
            element.bind('click', account_click)
    except: pass


def bind_all_header_footer_links(ev):
    elements = []
    elements.append(document['contact_link'].bind('click', contact_link_click))
    elements.append(document['logo_link'].bind('click', logo_link_click))

    elements.append(document['header_running_link'].bind('click', products_link_click))
    elements.append(document['header_fitness_link'].bind('click', products_link_click))
    elements.append(document['header_tennis_link'].bind('click', products_link_click))
    elements.append(document['header_football_link'].bind('click', products_link_click))
    elements.append(document['header_golf_link'].bind('click', products_link_click))

    elements.append(document['footer_running_link'].bind('click', products_link_click))
    elements.append(document['footer_cycling_link'].bind('click', products_link_click))
    elements.append(document['footer_triathlon_link'].bind('click', products_link_click))
    elements.append(document['footer_fitness_link'].bind('click', products_link_click))
    elements.append(document['footer_tennis_link'].bind('click', products_link_click))
    elements.append(document['footer_more_sports_link'].bind('click', products_link_click))
    elements.append(document['footer_style_link'].bind('click', products_link_click))
    elements.append(document['footer_special_link'].bind('click', products_link_click))
    elements.append(document['footer_brand_events_link'].bind('click', products_link_click))
    for element in elements:
        try:
            element
        except: pass


def reload_page(ev):
    window.location.reload()


def is_login_error_message_visible(ev):
    if len(document.get(selector="span[id='invalid_acc'")) > 0:
        bind_login_button(ev)
        return True
    else:
        reload_page(ev)


def post_data(url, qs, callbacks=None):
    req = ajax.ajax()
    # Bind the complete State to the on_post_complete function
    req.bind('complete', lambda req:on_post_complete(req, callbacks))
    # send a POST request to the url
    req.open('POST', url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    # send data as a dictionary
    req.send(qs)


def get_data(url, qs, callbacks=None):
    req = ajax.ajax()
    req.bind('complete', lambda req:on_get_complete(req, callbacks))
    # Bind the complete State to the on_get_complete function
    req.open('GET', url+'?'+qs, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.send()


def on_post_complete(req, callbacks=None):
    if req.status == 200 or req.status == 0:
        #  Take our response and inject it into the html div with id='main'
        document["main_area"].html = req.text
        if callbacks is not None:
            for callback in callbacks:
                callback(req)
    else:
        document["main_area"].html = "error " + req.text


def on_get_complete(req, callbacks=None):
    if req.status == 200 or req.status == 0:
        #  Take our response and inject it into the html div with id='main'
        document["main_area"].html = req.text
        if callbacks is not None:
            for callback in callbacks:
                callback(req)
        bind_my_acc_button(req)
        bind_register_link(req)
        bind_register_footer_link(req)
        bind_register_button(req)
        bind_post_review_button(req)
        try:
            for product in document['all_products'].get(selector="a[id*='single_page_product_'"):
                bind_single_product_link(req, product)
        except KeyError: pass
        # try:
        #     for link in document['main_wrapper'].get(selector="li[class*='go_to_404'"):
        #         bind_404_link(req, link)
        # except KeyError: pass
        # try:
        #     for link in document['main_wrapper'].get(selector="a[class*='go_to_404'"):
        #         bind_404_link(req, link)
        # except KeyError: pass
        # try:
        #     for link in document['main_wrapper'].get(selector="a[class*='page_500'"):
        #         bind_500_link(req, link)
        # except KeyError: pass
        # bind_all_header_footer_links(req)
        bind_logout_button(req)
    else:
        document["main_area"].html = "error " + req.text


def contact_link_click(ev):
    get_data("/contact", qs)


def logo_link_click(ev):
    get_data("/main_page", qs)


def products_link_click(ev):
    get_data("/products_page", qs)


def products_id_click(ev):
    id = (ev.currentTarget.id).split("_")[3]
    get_data("/single_product", "product={}".format(id))


def link_404_click(ev):
    get_data("/page_404", qs)


def link_500_click(ev):
    get_data("/page_500", qs)


def register_button_click(ev):
    _firstName = document['inputFirstName'].value
    _lastName = document['inputLastName'].value
    _email = document['inputEmail'].value
    _password = document['inputPassword'].value
    callback = [bind_login_button]
    qs = {'inputFirstName': _firstName,
          'inputLastName': _lastName,
          'inputEmail': _email,
          'inputPassword': _password}
    post_data("/register_action", qs, callback)


def review_button_click(ev):
    _stars = document['star_input'].value
    _post = document['area'].value
    _prod_id = document['pppuid'].value.split("-")[0]
    _user_id = document['pppuid'].value.split("-")[1]
    callback = [bind_post_review_button]
    if len(_post) < 1:
        return
    qs = {'stars': _stars,
          'post_area': _post,
          'prod_id': _prod_id,
          'user_id': _user_id}
    post_data("/post_review_action", qs, callback)


def login_button_click(ev):
    _email = document['login_email'].value
    _password = document['login_password'].value
    callback = [is_login_error_message_visible, bind_logout_button, bind_my_acc_button]
    qs = {'login_email': _email,
          'login_password': _password}
    post_data("/login_action", qs, callback)


def logout_click(ev):
    callback = [reload_page]
    get_data("/logout", qs, callback)


def account_click(ev):
    callbacks = [bind_register_link, bind_login_button]
    get_data("/account", qs, callbacks)


def register_link_click(ev):
    callbacks = [bind_register_button]
    get_data("/register", qs, callbacks)

try:
    for element in document.get(selector="li[id*='myacc_'"):
        element.bind('click', account_click)
except: pass


bind_register_link()
bind_logout_button()
document['contact_link'].bind('click', contact_link_click)
document['logo_link'].bind('click', logo_link_click)

document['footer_signup'].bind('click', register_link_click)

document['header_running_link'].bind('click', products_link_click)
document['header_fitness_link'].bind('click', products_link_click)
document['header_tennis_link'].bind('click', products_link_click)
document['header_football_link'].bind('click', products_link_click)
document['header_golf_link'].bind('click', products_link_click)

document['footer_running_link'].bind('click', products_link_click)
document['footer_cycling_link'].bind('click', products_link_click)
document['footer_triathlon_link'].bind('click', products_link_click)
document['footer_fitness_link'].bind('click', products_link_click)
document['footer_tennis_link'].bind('click', products_link_click)
document['footer_more_sports_link'].bind('click', products_link_click)
document['footer_style_link'].bind('click', products_link_click)
document['footer_special_link'].bind('click', products_link_click)
document['footer_brand_events_link'].bind('click', products_link_click)

# for link in document['main_wrapper'].get(selector="li[class*='go_to_404'"):
#     link.bind('click', link_404_click)
#
# for link in document['main_wrapper'].get(selector="a[class*='go_to_404'"):
#     link.bind('click', link_404_click)
#
# for link in document['main_wrapper'].get(selector="a[class*='page_500'"):
#     link.bind('click', link_500_click)