from sqlalchemy import text
from flask import Flask, request, render_template
from app import app
from app import db

@app.route('/report', methods=['GET', 'POST'])
def report():
    results = []
    if request.method == 'POST':
        pet_type = request.form['type']
        min_age = request.form['min_age']
        max_age = request.form['max_age']
        sql = text("""
            SELECT type, COUNT(*) as count, AVG(age) as avg_age
            FROM pet
            WHERE type = :type AND age BETWEEN :min_age AND :max_age
            GROUP BY type
        """)
        results = db.session.execute(sql, {
            'type': pet_type,
            'min_age': min_age,
            'max_age': max_age
        }).fetchall()
    return render_template('report.html', results=results)
