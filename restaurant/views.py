import re
import time
import uuid

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from django.conf import settings
from django.db.models import F, Count
from django.http import Http404
from django.shortcuts import render, redirect
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from .models import *


def home(request):
	items_per_page = 6
	try:
		restaurants = Business.objects.all().order_by('-stars', '-review_count')[:items_per_page]
	except Attributes.DoesNotExist:
		restaurants = Business.objects.all().order_by('-stars', '-review_count')
	try:
		username = request.session['user_name']
		user_id = request.session['user_id']
		user = User.objects.get(user_id=user_id)
	except KeyError:
		username = None
		user = None
	total = Business.objects.count()
	items = 1
	if total > 2 * items_per_page:
		items = 3
	elif total > items_per_page:
		items = 2
	try:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')[:10]
	except Categories.DoesNotExist:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')
	
	context = {
		'username': username,
		'restaurants': restaurants,
		'categories': categories,
		'items': items,
		'activity': 'home',
		'user': user
	}
	
	return render(request, 'home.html', context=context)


def home2(request, pid):
	pid = int(pid)
	if pid < 1:
		raise Http404()
	elif pid == 1:
		return redirect('home')
	try:
		username = request.session['user_name']
		user_id = request.session['user_id']
		user = User.objects.get(user_id=user_id)
	except KeyError:
		username = None
		user = None
	try:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')[:10]
	except Categories.DoesNotExist:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')
	total = Business.objects.count()
	items_per_page = 6
	last = False
	if items_per_page * pid < total:
		restaurants = Business.objects.all().order_by('-stars', '-review_count')[
		              items_per_page * (pid - 1):items_per_page * pid]
	elif items_per_page * (pid - 1) < total:
		restaurants = Business.objects.all().order_by('-stars', '-review_count')[items_per_page * (pid - 1):]
		last = True
	else:
		raise Http404()
	
	context = {
		'username': username,
		'restaurants': restaurants,
		'categories': categories,
		'activity': 'home',
		'current': pid,
		'last': last,
		'user': user
	}
	
	return render(request, 'home2.html', context=context)


def search(request):
	try:
		username = request.session['user_name']
		user_id = request.session['user_id']
		user = User.objects.get(user_id=user_id)
	except KeyError:
		username = None
		user = None
	try:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')[:10]
	except Categories.DoesNotExist:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')
	categories_set = categories.values_list('categories', flat=True)
	if request.method == 'POST':
		content = request.POST['search']
		content = content.strip()
		star = request.POST['star']
		try:
			star = int(star)
		except ValueError:
			star = float(star)
		selected_category = request.POST['category']
		selected_price = request.POST['price']
		if selected_price != '':
			selected_price = int(selected_price)
		request.session['content'] = content
		request.session['star'] = star
		request.session['selected_category'] = selected_category
		request.session['selected_price'] = selected_price
	else:
		try:
			content = request.session['content']
			star = request.session['star']
			selected_category = request.session['selected_category']
			selected_price = request.session['selected_price']
		except KeyError:
			return redirect('home')
	name = re.split('#', content)[0].strip()
	if name != '':
		restaurants = Business.objects.filter(name__icontains=name)
	else:
		restaurants = Business.objects.all()
	if selected_category != '':
		if selected_category == 'Other':
			for el in categories_set:
				restaurants = restaurants.exclude(categories__categories=el)
		else:
			restaurants = restaurants.filter(categories__categories=selected_category)
	restaurants = restaurants.filter(stars__lte=star).order_by('-stars', '-review_count')
	if selected_price != '':
		restaurants = restaurants.filter(attributes__RestaurantsPriceRange2=selected_price)
	if '#' in content:
		tags = re.split('#', content)[1]
		for tag in re.split(',', tags):
			tag = tag.strip()
			if re.search(tag, 'TakeOut', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsTakeOut=1)
			elif re.search(tag, 'Delivery', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsDelivery=1)
			elif re.search(tag, 'Reservations', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsReservations=1)
			elif re.search(tag, 'GoodForGroups', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsGoodForGroups=1)
			elif re.search(tag, 'OutdoorSeating', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__OutdoorSeating=1)
			elif re.search(tag, 'GoodForKids', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__GoodForKids=1)
			elif re.search(tag, 'TV', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__HasTV=1)
			elif re.search(tag, 'WiFi', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__WiFi=1)
			elif re.search(tag, 'BikeParking', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__BikeParking=1)
	
	total = restaurants.count()
	items_per_page = 6
	items = 1
	if total > 2 * items_per_page:
		items = 3
	elif total > items_per_page:
		items = 2
	if total >= items_per_page:
		restaurants = restaurants[:6]
	
	context = {
		'content': content,
		'star': star,
		'selected_category': selected_category,
		'selected_price': selected_price,
		'restaurants': restaurants,
		'username': username,
		'categories': categories,
		'activity': 'search for : \"' + content + '\"',
		'items': items,
		'user': user
	}
	
	return render(request, 'search.html', context=context)


def search2(request, pid):
	pid = int(pid)
	if pid < 1:
		raise Http404()
	elif pid == 1:
		return redirect('search')
	try:
		username = request.session['user_name']
		user_id = request.session['user_id']
		user = User.objects.get(user_id=user_id)
	except KeyError:
		username = None
		user = None
	try:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')[:10]
	except Categories.DoesNotExist:
		categories = Categories.objects.all().values('categories').annotate(total=Count('categories')).order_by(
			'-total')
	categories_set = categories.values_list('categories', flat=True)
	if request.method == 'POST':
		content = request.POST['search']
		content = content.strip()
		star = request.POST['star']
		try:
			star = int(star)
		except ValueError:
			star = float(star)
		selected_category = request.POST['category']
		selected_price = request.POST['price']
		if selected_price != '':
			selected_price = int(selected_price)
		print(type(selected_price))
		request.session['content'] = content
		request.session['star'] = star
		request.session['selected_category'] = selected_category
		request.session['selected_price'] = selected_price
	else:
		try:
			content = request.session['content']
			star = request.session['star']
			selected_category = request.session['selected_category']
			selected_price = request.session['selected_price']
		except KeyError:
			return redirect('home')
	name = re.split('#', content)[0].strip()
	if name != '':
		restaurants = Business.objects.filter(name__icontains=name)
	else:
		restaurants = Business.objects.all()
	if selected_category != '':
		if selected_category == 'Other':
			for el in categories_set:
				restaurants = restaurants.exclude(categories__categories=el)
		else:
			restaurants = restaurants.filter(categories__categories=selected_category)
	restaurants = restaurants.filter(stars__lte=star).order_by('-stars', '-review_count')
	if selected_price != '':
		restaurants = restaurants.filter(attributes__RestaurantsPriceRange2=selected_price)
	if '#' in content:
		tags = re.split('#', content)[1]
		for tag in re.split(',', tags):
			tag = tag.strip()
			if re.search(tag, 'TakeOut', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsTakeOut=1)
			elif re.search(tag, 'Delivery', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsDelivery=1)
			elif re.search(tag, 'Reservations', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsReservations=1)
			elif re.search(tag, 'GoodForGroups', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__RestaurantsGoodForGroups=1)
			elif re.search(tag, 'OutdoorSeating', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__OutdoorSeating=1)
			elif re.search(tag, 'GoodForKids', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__GoodForKids=1)
			elif re.search(tag, 'TV', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__HasTV=1)
			elif re.search(tag, 'WiFi', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__WiFi=1)
			elif re.search(tag, 'BikeParking', re.IGNORECASE):
				restaurants = restaurants.filter(attributes__BikeParking=1)
	
	total = restaurants.count()
	items_per_page = 6
	last = False
	if items_per_page * pid < total:
		restaurants = restaurants[items_per_page * (pid - 1):items_per_page * pid]
	elif items_per_page * (pid - 1) < total:
		restaurants = restaurants[items_per_page * (pid - 1):]
		last = True
	else:
		raise Http404()
	
	context = {
		'content': content,
		'star': star,
		'selected_category': selected_category,
		'selected_price': selected_price,
		'restaurants': restaurants,
		'username': username,
		'categories': categories,
		'activity': 'search for : \"' + content + '\"',
		'current': pid,
		'last': last,
		'user': user
	}
	
	return render(request, 'search2.html', context=context)


def login(request):
	try:
		request.session['user_id']
		return redirect('home')
	except KeyError:
		return render(request, 'login.html', {'message': None})


def logout(request):
	request.session.flush()
	return redirect('login')


def validation(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return render(request, 'login.html', {'message': 'user does not exist'})
		if user.password == password:
			request.session['user_id'] = user.user_id
			request.session['user_email'] = email
			request.session['user_name'] = user.name
			return redirect('home')
		else:
			return render(request, 'login.html', {'message': 'wrong password, try again', 'email': email})
	else:
		raise Http404('No permission')


def register(request):
	if request.method == 'POST':
		name = request.POST['reg-name']
		email = request.POST['reg-email']
		password = request.POST['reg-password']
		if name.strip() == '':
			return render(request, 'login.html', {'reg_message': 'name requires', 'reg_flag': True})
		if email.strip() == '':
			return render(request, 'login.html', {'reg_message': 'email requires', 'reg_flag': True})
		elif '@' not in email:
			return render(request, 'login.html', {'reg_message': 'email missing an \'@\'', 'reg_flag': True})
		if password.strip() == '':
			return render(request, 'login.html', {'reg_message': 'password requires', 'reg_flag': True})
		if len(password) > 20:
			return render(request, 'login.html', {'reg_message': 'password too long (20)', 'reg_flag': True})
		try:
			User.objects.get(email=email)
			return render(request, 'login.html', {'reg_message': 'user exists', 'reg_flag': True})
		except User.DoesNotExist:
			User.objects.create(user_id=get_uuid(), name=name, review_count=0, yelping_since=localtime(), fans=0,
			                    average_stars=0, email=email, password=password, positive_votes=0, negative_votes=0)
			return render(request, 'login.html', {'success': True, 'email': email})
	else:
		return render(request, 'login.html', {'reg_flag': True})


def top(request):
	try:
		username = request.session['user_name']
		user_id = request.session['user_id']
		user = User.objects.get(user_id=user_id)
	except KeyError:
		username = None
		user = None
	tres = Business.objects.annotate(
		average_rating=600 * (F('stars') - 4) - 600 * (3 - F('stars')) + F('review_count')).values('business_id',
	                                                                                               'name').order_by(
		'-average_rating')[:8]
	tag = User.objects.annotate(
		average_rating=F('positive_votes') - F('negative_votes') + 3 * F('review_count')).order_by('-average_rating')[
	      :8]
	trev = Business.objects.annotate(average_rating=F('review_count')).order_by('-average_rating')[:8]
	trat = Business.objects.annotate(average_rating=F('stars')).filter(review_count__gt=50).order_by('-average_rating')[
	       :8]
	content = {
		'users': tag,
		'busname': tres,
		'trevname': trev,
		'tratname': trat,
		'username': username,
		'activity': 'top users & restaurants',
		'user': user
	}
	return render(request, 'top.html', context=content)


def detail(request, business_id):
	try:
		username = request.session['user_name']
		user_id = request.session['user_id']
		user = User.objects.get(user_id=user_id)
	except KeyError:
		username = None
		user = None
	p1 = business_id
	a = []
	da = Checkin.objects.filter(business_id__exact=p1).values_list('date', flat=True)
	k = 0
	for _ in da:
		a.append((da[k].hour))
		k = k + 1
	plt.hist(a)
	plt.title("Active Hours")
	plt.savefig(settings.BASE_DIR + '/static/img/log.png')
	plt.close()
	
	reviews = Review.objects.filter(business_id__exact=p1).order_by("-review_date")[:6]
	word = Review.objects.filter(business_id__exact=p1).values_list('text', flat=True)
	b = []
	j = 0
	for _ in word:
		b.append(word[j])
		j = j + 1
	text = ' '.join(b)
	alice_coloring = np.array(Image.open(settings.BASE_DIR + "/static/img/666.jpg"))
	stopwords = set(STOPWORDS)
	wc = WordCloud(background_color="white", max_words=300, mask=alice_coloring,
	               stopwords=stopwords, max_font_size=50, random_state=42)
	wc.generate(text)
	image_colors = ImageColorGenerator(alice_coloring)
	plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
	plt.axis("off")
	plt.savefig(settings.BASE_DIR + '/static/img/wordcloud.png', transparent=True)
	plt.close()
	
	c = []
	s = 0
	rate = Review.objects.filter(business_id__exact=p1).values_list('stars', flat=True)
	for _ in rate:
		c.append(rate[s])
		s = s + 1
	dict = {5: 1, 4: 1, 3: 1, 2: 1, 1: 1}
	for key in c:
		dict[key] = dict.get(key, 0) + 1
	t = []
	s = 1
	for _ in dict:
		t.append(dict[s])
		s = s + 1
	plt.barh(range(5), t, height=0.7, color='pink', alpha=0.8)
	plt.yticks(range(5), [1, 2, 3, 4, 5])
	plt.title("Rating")
	plt.savefig(settings.BASE_DIR + '/static/img/rate.png')
	plt.close()
	
	rev = Review.objects.filter(business_id__exact=p1).values_list('stars', flat=True)
	
	detail = Business.objects.filter(business_id__exact=p1)
	bus_name = detail[0].name
	bus_city = detail[0].city
	bus_address = detail[0].address
	bus_state = detail[0].state
	bus_zip = detail[0].postal_code
	bus_stars = detail[0].stars
	attr = Attributes.objects.filter(business_id__exact=p1)
	price = attr[0].RestaurantsPriceRange2
	price = price * '$'
	cate = Categories.objects.filter(business_id__exact=p1).values('categories')[:4]
	cates = Attributes.objects.filter(business_id__exact=p1).values('RestaurantsTakeOut', 'RestaurantsDelivery',
	                                                                'RestaurantsReservations', 'OutdoorSeating', 'WiFi')
	k = []
	if cates[0]['RestaurantsTakeOut']:
		k.append("✔")
	else:
		k.append("×")
	if cates[0]['RestaurantsDelivery']:
		k.append("✔")
	else:
		k.append("×")
	if cates[0]['RestaurantsReservations']:
		k.append("✔")
	else:
		k.append("×")
	if cates[0]['OutdoorSeating']:
		k.append("✔")
	else:
		k.append("×")
	if cates[0]['WiFi']:
		k.append("✔")
	else:
		k.append("×")
	
	collec = Collections.objects.filter(business_id_id__exact=p1).annotate(Countid=Count('id')).values('Countid')
	m = len(collec)
	
	context = {"bus_name": bus_name,
	           "bus_city": bus_city,
	           "bus_address": bus_address,
	           "bus_state": bus_state,
	           "bus_zip": bus_zip,
	           "bus_stars": bus_stars,
	           "price": price,
	           "cate": cate,
	           "cates": k,
	           "coll": m,
	           "reviews": reviews,
	           'username': username,
	           'activity': 'detail: ' + bus_name,
	           'user': user
	           }
	return render(request, 'detail.html', context=context)


def searchMap(request):
	return render(request, 'searchmap.html')


def usrshow(request, user_id):
	try:
		user_idv = request.session['user_id']
	except KeyError:
		username = None
		user_idv = 0
		userv = None
	if user_idv == 0:
		userv = None
	else:
		try:
			userv = User.objects.get(user_id=user_idv)
		except KeyError:
			userv = None
	user = User.objects.get(user_id=user_id)
	reviews = Review.objects.filter(user_id=user_id).order_by('-review_date')[:3]
	collections = Collections.objects.filter(user_id=user_id)[:3]
	content = {
		'userv': userv,
		'user': user,
		'reviews': reviews,
		'collections': collections,
	}
	return render(request, 'usershow.html', context=content)


def userinf(request):
	error = None
	try:
		user_id = request.session['user_id']
	
	except KeyError:
		username = None
		user = None
	
	try:
		user = User.objects.get(user_id=user_id)
		reviews = Review.objects.filter(user_id=user_id)
		collections = Collections.objects.filter(user_id=user_id)
		name = user.name
		password = user.password
		email = user.email
	
	except User.DoesNotExist:
		return render(request, 'login.html', {'message': 'user does not exist'})
	if request.method == 'POST':
		name = request.POST['reg-name']
		email = request.POST['reg-email']
		password = request.POST['reg-password']
		error = None
		content = {
			'username': name,
			'user_id': user_id,
			'email': email,
			'password': password,
			'reviews': reviews,
			'collections': collections,
			'error': error,
			
		}
		if name.strip() == '':
			error = 'name missing'
			content = {
				'username': name,
				'user_id': user_id,
				'email': email,
				'password': password,
				'reviews': reviews,
				'collections': collections,
				'error': error,
				
			}
			return render(request, 'user.html', context=content)
		if email.strip() == '':
			error = 'email requires'
			content = {
				'username': name,
				'user_id': user_id,
				'email': email,
				'password': password,
				'reviews': reviews,
				'collections': collections,
				'error': error,
				
			}
			return render(request, 'user.html', context=content)
		elif '@' not in email:
			error = 'email missing an \'@\''
			content = {
				'username': name,
				'user_id': user_id,
				'email': email,
				'password': password,
				'reviews': reviews,
				'collections': collections,
				'error': error,
				
			}
			return render(request, 'user.html', context=content)
		if password.strip() == '':
			error = 'password requires'
			content = {
				'username': name,
				'user_id': user_id,
				'email': email,
				'password': password,
				'reviews': reviews,
				'collections': collections,
				'error': error,
				
			}
			return render(request, 'user.html', context=content)
		if len(password) > 20:
			error = 'password too long (20)'
			content = {
				'username': name,
				'user_id': user_id,
				'email': email,
				'password': password,
				'reviews': reviews,
				'collections': collections,
				'error': error,
				
			}
			return render(request, 'user.html', context=content)
		try:
			usr2 = User.objects.get(email=email)
			if usr2.user_id != user_id:
				error = 'email exists'
				content = {
					'username': name,
					'user_id': user_id,
					'email': email,
					'password': password,
					'reviews': reviews,
					'collections': collections,
					'error': error,
					
				}
				return render(request, 'user.html', context=content)
			else:
				User.objects.filter(user_id=user_id).update(name=name, email=email, password=password)
				request.session['user_name'] = name
				request.session['user_email'] = email
				error = 'success'
				content = {
					'username': name,
					'user_id': user_id,
					'email': email,
					'password': password,
					'reviews': reviews,
					'collections': collections,
					'error': error,
					
				}
				return render(request, 'user.html', context=content)
		except User.DoesNotExist:
			User.objects.filter(user_id=user_id).update(name=name, email=email, password=password)
			request.session['user_name'] = name
			request.session['user_email'] = email
			error = 'success'
			content = {
				'username': name,
				'user_id': user_id,
				'email': email,
				'password': password,
				'reviews': reviews,
				'collections': collections,
				'error': error,
				
			}
			return render(request, 'user.html', context=content)
	content = {
		'username': name,
		'user_id': user_id,
		'email': email,
		'password': password,
		'reviews': reviews,
		'collections': collections,
		'error': error,
	}
	return render(request, 'user.html', context=content)


def analysis(request):
	return render(request, 'Analyst category zipcode area population.html')


def yelp_visualize(request):
	return render(request, 'Yelp_Visualize.html')


def localtime():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_uuid():
	return uuid.uuid4().hex
