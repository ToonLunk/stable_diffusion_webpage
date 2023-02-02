from libs.requirements import *
from libs.stable_diffusion_funcs import generate_image
from libs.get_filename import getFilename
from forms import getPrompt

app = Flask(__name__)

# for using forms
app.config['SECRET_KEY'] = 'a00e4dd49c51af8d6f8368d7eef2ffea'

#  route for the home page
@app.route("/", methods=['GET', 'POST'])
def generate():
    form = getPrompt()
    try:
        # get the past prompts from ./extras/prompts.txt
        with open("./extras/prompts.txt", "r") as f:
            pastPrompts = f.read()
            pastPrompts = pastPrompts.split("\n")
            pastPrompts = pastPrompts[:-1] # remove the last empty string
            # get the last 10 prompts, with the most recent at the top, only show unique prompts
            pastPrompts = list(dict.fromkeys(pastPrompts))
            print(pastPrompts)
    except:
        print("WARNING: Exception reading ./extra/prompts.txt, maybe it doesn't exist yet?")
        pastPrompts = []

    try:
        # get the past images from ./static/img/output
        pastImages = os.listdir("./static/img/output")
        print(pastImages)
    except:
        print("WARNING: Exception reading ./static/img/output, maybe it doesn't exist yet?")
        pastImages = []
    
    # define request
    request = flask.request

    # if a get request is made, get the prompt from URL
    if request.method == 'GET':
        prompt = request.args.get('prompt')
        if prompt:
            print("user's prompt: ", prompt)

            # get the filename
            fileName = getFilename(prompt)

            # add file prompt to pastPrompts
            pastPrompts.append(prompt)

            # generate image, show progress bar
            generate_image(prompt, fileName=fileName)

            # add file name to pastImages
            pastImages.append(f"{fileName}.png")

            return render_template('index.html', form=form, pastPrompts=pastPrompts, pastImages=pastImages, fileName=fileName)
        else:
            return render_template('index.html', form=form, pastPrompts=pastPrompts, pastImages=pastImages)

    if form.validate_on_submit():
        prompt = form.prompt.data
        print("user's prompt: ", prompt)

        # get the filename
        fileName = getFilename(prompt)

        # add file prompt to pastPrompts
        pastPrompts.append(prompt)

        # generate image, show progress bar
        generate_image(prompt, fileName=fileName)

        # add file name to pastImages
        pastImages.append(f"{fileName}.png")

        return render_template('index.html', form=form, pastPrompts=pastPrompts, pastImages=pastImages, fileName=fileName)
    else:
        return render_template('index.html', form=form, pastPrompts=pastPrompts, pastImages=pastImages)

# to not have to restart the server every time you make a change
if __name__ == "__main__":
    app.run(host="0.0.0.0")
    input("Press Enter to exit...")