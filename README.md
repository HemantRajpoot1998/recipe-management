# recipe-management
##For Users

Create new recipes with details like:
Title
Description
Ingredients
Steps
Image upload
View all recipes
Search and filter recipes
Edit existing recipes
Delete recipes

🔐 Authentication
Login / logout
Only authenticated users can create, update, or delete recipes

git clone https://github.com/HemantRajpoot1998/recipe-management.git
cd recipe-management

pip install -r requirements.txt
python manage.py runserver


celery -A project worker --loglevel=info

##Excel File Format (Very Important)

##Your Excel file must have 3 sheets:

#Sheet 1 → recipes

title	  description	    prep_duration	cook_duration	thumbnail_url

Chocolate Cake	Rich cake	15	                30	        http://img.com/cake.jpg
Pizza	  Cheese pizza	    20	                25	        http://img.com/pizza.jpg

#Sheet 2 → ingredients
recipe_title	name	        picture_url

Chocolate Cake	Flour	        http://img.com/flour.jpg
Chocolate Cake	Cocoa Powder	http://img.com/cocoa.jpg
Pizza	        Cheese	        http://img.com/cheese.jpg

#Sheet 3 → steps
recipe_title	order	description	        image_url

Chocolate Cake	1	Mix ingredients	        http://img.com/s1.jpg
Chocolate Cake	2	Bake in oven	        http://img.com/s2.jpg
Pizza	        1	Prepare dough	http://img.com/p1.jpg
