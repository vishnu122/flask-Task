# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
# if __name__ == '__main__':
#     app.run()


from flask import Flask, request, render_template_string, abort
import os
import linecache

app = Flask(__name__)


# @app.route('/')
# def home():
#     return "Welcome to my homepage!"
@app.route('/', defaults={'filename': 'file1.txt'})
@app.route('/<filename>', methods=['GET'])
def read_file(filename='file1.txt'):
    try:
        # Make sure the file exists
        if not os.path.exists(filename):
            abort(404, description="Resource not found")

        # Check for optional start and end line numbers in the query string
        start_line = request.args.get('start_line', default=1, type=int)
        end_line = request.args.get('end_line', default=None, type=int)

        # Try different encodings
        for encoding in ['utf-8', 'utf-16', 'utf-32']:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    lines = file.readlines()[start_line - 1:end_line]
                break
            except UnicodeDecodeError:
                pass
        else:
            abort(500, description="Failed to decode file with utf-8, utf-16, or utf-32.")

        # Render the lines in a simple HTML template
        return render_template_string('<html><body><pre>{{ contents|safe }}</pre></body></html>', contents=''.join(lines))

    except Exception as e:
        abort(500, description=str(e))

if __name__ == "__main__":
    app.run(debug=True)

