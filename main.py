from flask import request, render_template, Flask, redirect, url_for
from get_instagram import insta_site

app = Flask(__name__)


@app.route("/<string:search_input>", methods=["GET", "POST"])
# @app.route("/search_result?search_input=", methods=["GET", "POST"])
def search_result(search_input):
	if request.method == "POST":
		search_input = request.form["search_input"]
		search_input = search_input.lower().strip()
		return redirect(url_for(".search_result", search_input=search_input))
	site = insta_site(search_input)
	if site.status_code:
		img_path = '/' + site.get_img()
		followers, following, posts, description = site.get_info()
		print(img_path)
		return render_template('search_result.html', name=search_input, followers=followers, following=following, posts=posts, img_path=img_path)
	else:
		return 'Error!'


@app.route("/", methods=["GET", "POST"])
def main():
	from test_request import test
	search_input = ""
	
	if request.method == "POST":
		search_input = request.form["search_input"]
		search_input = search_input.lower().strip()
		
	if search_input == "":
		return render_template('home.html')		
	else:
		return redirect(url_for(".search_result", search_input=search_input))
	

# Running on http://127.0.0.1:5000/
if __name__ == "__main__":
	app.run(debug=True)

