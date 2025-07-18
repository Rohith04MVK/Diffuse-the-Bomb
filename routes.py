# routes.py (NEW FILE)
from flask import Blueprint, render_template, redirect, url_for, flash, Response, request, session
from datetime import datetime
from functools import wraps
from extensions import db
from models import User, Puzzle
from puzzle_generator import PuzzleGenerator

main_bp = Blueprint('main', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please identify yourself to continue the mission.", "info")
            return redirect(url_for('main.entry_page'))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/', methods=['GET', 'POST'])
def entry_page():
    # This logic is identical to the previous version, just using the blueprint
    if 'user_id' in session and request.method == 'GET':
        return redirect(url_for('main.briefing_page'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            flash("Username cannot be empty.", "incorrect")
            return redirect(url_for('main.entry_page'))
        user = User.query.filter_by(username=username).first()
        if user:
            flash(f"Welcome back, Agent {user.username}.", "correct")
        else:
            user = User(username=username)
            db.session.add(user)
            generator = PuzzleGenerator()
            all_puzzles_data = generator.generate_all_puzzles()
            for level, puzzle_data in all_puzzles_data.items():
                puzzle = Puzzle(level=level, input_data=puzzle_data.input,
                                solution=puzzle_data.output, author=user)
                db.session.add(puzzle)
            db.session.commit()
            flash(
                f"New agent profile for {user.username} created. Mission begins now!", "correct")
        session['user_id'] = user.id
        return redirect(url_for('main.briefing_page'))
    return render_template('entry.html', title='Agent Identification')


@main_bp.route('/briefing')
@login_required
def briefing_page():
    user = User.query.get(session['user_id'])
    if user.end_time:
        return redirect(url_for('main.finished'))
    return render_template('briefing.html', user=user, title='Mission Briefing')


@main_bp.route('/challenge')
@login_required
def challenge_page():
    # All other routes from the previous app.py go here
    # Just remember to prefix url_for with 'main.' -> url_for('main.finished')
    user = User.query.get(session['user_id'])
    if user.end_time:
        return redirect(url_for('main.finished'))
    solved_levels = [p.level for p in user.puzzles if p.is_solved]
    active_level = len(solved_levels) + 1
    return render_template('challenge.html', puzzles=user.puzzles.order_by(Puzzle.level).all(), solved_levels=solved_levels, active_level=active_level, user=user)


@main_bp.route('/submit/<int:level_num>', methods=['POST'])
@login_required
def submit_answer(level_num):
    user = User.query.get(session['user_id'])
    user_answer = request.form.get('answer', '').strip()
    puzzle = user.puzzles.filter_by(level=level_num).first_or_404()
    if user_answer == puzzle.solution:
        puzzle.is_solved = True
        num_solved = user.puzzles.filter_by(is_solved=True).count()
        if num_solved == user.puzzles.count():
            user.end_time = datetime.utcnow()
            flash("BOMB DEFUSED! City saved. Excellent work, Agent.", "correct")
            db.session.commit()
            return redirect(url_for('main.finished'))
        else:
            flash(
                f"Layer {level_num} disabled. Accessing next level...", "correct")
        db.session.commit()
    else:
        flash("Incorrect code. Security layer remains active. Try again.", "incorrect")
    return redirect(url_for('main.challenge_page'))


@main_bp.route('/finished')
@login_required
def finished():
    user = User.query.get(session['user_id'])
    if not user.end_time:
        return redirect(url_for('main.challenge_page'))
    return render_template('finished.html', user=user)


@main_bp.route('/leaderboard')
def leaderboard():
    finished_users = User.query.filter(User.end_time.isnot(None)).all()
    sorted_users = sorted(finished_users, key=lambda u: u.end_time -
                          u.start_time if u.end_time and u.start_time else datetime.max)
    return render_template('leaderboard.html', users=sorted_users)


@main_bp.route('/input/<int:level_num>')
@login_required
def get_input_file(level_num):
    user = User.query.get(session['user_id'])
    puzzle = user.puzzles.filter_by(level=level_num).first_or_404()
    return Response(puzzle.input_data, mimetype="text/plain", headers={"Content-disposition": f"attachment; filename=level_{level_num}_input.txt"})


@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main.entry_page'))