from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Cricketdb_owner:OVUrfTso39FN@ep-old-cherry-a1fwhrz9.ap-southeast-1.aws.neon.tech/Cricketdb?sslmode=require'
db = SQLAlchemy(app)

app.app_context().push()


# Define the models for our tables
class Table1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(100))
    runs = db.Column(db.Integer, default=0)


class Table2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name2 = db.Column(db.String(100))
    wickets = db.Column(db.Integer, default=0)


class Table3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name3 = db.Column(db.String(100))
    fifties = db.Column(db.Integer, default=0)


# Drop existing tables to ensure a clean start

#db.drop_all()

# Recreate the tables based on the model definitions
db.create_all()


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/submit_runs', methods=['POST'])
def submit():
    # Get data from the user
    name1 = request.form['name1']
    runs = request.form['runs']
    player = Table1.query.filter_by(name1=name1).first()
    if player:
        player.runs += int(runs)

    else:
        new_player = Table1(name1=name1, runs=runs)
        db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('show_table1'))


@app.route('/submit_wickets', methods=['POST'])
def submit2():
    # Get data from the user
    name2 = request.form['name2']
    wickets = request.form['wickets']
    player = Table2.query.filter_by(name2=name2).first()
    if player:
        player.wickets += int(wickets)

    else:
        new_player = Table2(name2=name2, wickets=wickets)
        db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('show_table2'))


@app.route('/submit_fifties', methods=['POST'])
def submit3():
    # Get data from the user
    name3 = request.form['name3']
    fifties = request.form['fifties']
    player = Table3.query.filter_by(name3=name3).first()
    if player:
        player.fifties += int(fifties)

    else:
        new_player = Table3(name3=name3, fifties=fifties)
        db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('show_table3'))


@app.route('/show_table1')
def show_table1():
    # Fetch data from Table1
    table1_data = Table1.query.order_by(Table1.runs.desc()).limit(5).all()
    #table1_data = Table1.query.all()
    return render_template('show_table1.html', table1_data=table1_data)

@app.route('/more_runs', methods=['POST'])
def more_runs():
    # Fetch data from Table1
    #table1_data = Table1.query.order_by(Table1.runs.desc()).limit(5).all()
    table1_data = Table1.query.order_by(Table1.runs.desc()).all()
    return render_template('more_runs.html', table1_data=table1_data)

@app.route('/more_wickets', methods=['POST'])
def more_wickets():
    # Fetch data from Table1
    #table1_data = Table1.query.order_by(Table1.runs.desc()).limit(5).all()
    table1_data = Table2.query.order_by(Table2.wickets.desc()).all()
    return render_template('more_wickets.html', table1_data=table1_data)

@app.route('/more_50s', methods=['POST'])
def more_50s():
    # Fetch data from Table1
    #table1_data = Table1.query.order_by(Table1.runs.desc()).limit(5).all()
    table1_data = Table3.query.order_by(Table3.fifties.desc()).all()
    return render_template('more_50s.html', table1_data=table1_data)


@app.route('/show_table2')
def show_table2():
    # Fetch data from Table2
    table2_data = Table2.query.order_by(Table2.wickets.desc()).limit(5).all()
    return render_template('show_table2.html', table2_data=table2_data)


@app.route('/show_table3')
def show_table3():
    # Fetch data from Table2
    table3_data = Table3.query.order_by(Table3.fifties.desc()).limit(5).all()
    return render_template('show_table3.html', table3_data=table3_data)


# Create a Team model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    wins = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    @property
    def total_marks(self):
        return self.wins + self.draws + self.losses


@app.route('/prob')
def index2():
    teams = Team.query.all()
    return render_template('prob_index.html', teams=teams)


@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        wins = int(request.form['wins'])
        draws = int(request.form['draws'])
        losses = int(request.form['losses'])

        # Check if the team already exists
        existing_team = Team.query.filter_by(name=team_name).first()

        if existing_team:
            # Update the existing team
            existing_team.wins += wins
            existing_team.draws += draws
            existing_team.losses += losses
        else:
            # Create a new team
            new_team = Team(name=team_name, wins=wins, draws=draws, losses=losses)
            db.session.add(new_team)

        db.session.commit()

        return redirect(url_for('index2'))

    return render_template('prob_addteam.html')


# clear data


if __name__ == '__main__':
    app.run(debug=True)


