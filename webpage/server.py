from flask import Flask, request, redirect

app = Flask(__name__)

newid = 3
topics = [
    {'id':1, 'title':'html', 'body':'show html text'},
    {'id':2, 'title':'css', 'body':'show css text'}
]

def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
               {contents}
            </ol>
            {content}
            <ul>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def getcontents():
    liTags = ''
    for topic in topics:
        liTags += f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

@app.route('/')
def main():
    return template(getcontents(), '<ul><li><a href="/create/">create</a></li></ul>')

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getcontents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=["GET", "POST"])
def create():
    global newid
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getcontents, content)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': newid, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+str(newid)+'/'
        newid += 1
        return redirect(url)

@app.route('/update/<int:id>/', methods=["GET", "POST"])
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getcontents, content)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/'+str(id)+'/'
        return redirect(url)

@app.route('/delete/<int:id>/', methods=["POST"])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

app.run(port=1235, debug=True)