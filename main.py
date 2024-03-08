from flask import Flask,render_template,request,redirect,url_for,flash
from flask_bootstrap import Bootstrap5  #pip install bootstrap-flask
import numpy
from PIL import Image,ImageOps  #pip install pillow
import os
from werkzeug.utils import secure_filename
from datetime import date


app=Flask(__name__)
app.config["SECRET_KEY"]="willbeinDubai"

upload_dir="static/images/"

bootstrap=Bootstrap5(app)

@app.route('/',methods=["GET","POST"])
def home():
    current_year=date.today().year

    def rgb_to_hex(rgb):
        hex_code="#%02x%02x%02x" % rgb
        return hex_code

    def show_most_hex(filepath):
        img=Image.open(filepath).convert("RGB")
        img_width,img_height=img.size

        if img_width>=400 or img_height>=400:
            img=ImageOps.scale(image=img,factor=0.2)
        elif img_width>=600 or img_height>=600:
            img=ImageOps.scale(image=img, factor=0.4)
        elif img_width>=800 or img_height>=800:
            img=ImageOps.scale(image=img, factor=0.5)
        elif img_width>=1200 or img_height>=1200:
            img=ImageOps.scale(image=img,factor=0.6)

        img=ImageOps.posterize(image=img,bits=2) #Reduce the number of bits for each color channel(1-8,Bit 8 is the max bit can be used by the channel. The standard is bit 2.)
        # In every change of bit,change of colour contraction will be seen.

        img_array=numpy.array(img)
        unique_colors={}
        for column in img_array:
            for rgb in column:
                Rgb = tuple(rgb)
                if Rgb not in unique_colors:
                    unique_colors[Rgb]=1
                else:
                    unique_colors[Rgb] += 1

        sorted_unique_colors = sorted(unique_colors.items(), key=lambda color_tuple: color_tuple[1], reverse=True)
        print(sorted_unique_colors)

        colors_dict = dict(sorted_unique_colors)
        print(colors_dict)

        top_10_colors=list(colors_dict)[0:10]
        top_10_values = list(colors_dict.values())[0:10]
        total_values=sum(list(colors_dict.values()))

        print(total_values)
        print(top_10_colors)
        print(top_10_values)

        percent_list=[]
        for value in top_10_values:
            value_percent=(value/total_values)*100
            percent_list.append(round(value_percent,2))

        hex_list=[]
        for item in top_10_colors:
            hex=rgb_to_hex(item)
            hex_list.append(hex)

        return hex_list,percent_list

    if request.method=="POST":
        img_file=request.files.get("file")
        filename=secure_filename(img_file.filename)

        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif"):
            file_path=os.path.join(upload_dir,filename)
            img_file.save(file_path)
            hex,percent=show_most_hex(file_path)

            return render_template("index.html",image=file_path,display_img=True,color_list=hex,year=current_year,percent_list=percent)
        else:
            flash("Wrong file. Please upload an image.")
            return redirect(url_for("home"))

    return render_template("index.html",year=current_year)


if __name__=="__main__":
    app.run(debug=True)