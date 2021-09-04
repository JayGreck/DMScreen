from flaskdmscreen import app




# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['inputFile']

#     newFile = Statblock(statblock=file.filename, data=file.read())
#     db.session.add(newFile)
#     db.session.commit()

#     filename = file.read()


#     return render_template("base.html", filename=filename)

# @app.route('/display/<filename>')
# def display_image(filename):
#     return redirect(url_for('static', filename='uploads/' + filename, code=301))

if __name__ == "__main__":
    app.run(debug=True)