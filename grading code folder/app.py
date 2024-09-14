from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            prelim_grade = float(request.form['prelim_grade'])
            if prelim_grade < 0 or prelim_grade > 100:
                error = "Please enter a valid Prelim grade between 0 and 100."
                return render_template('index.html', error=error)
            
            required_percentage = calculate_required_percentage(prelim_grade)
            if isinstance(required_percentage, str):  # Error message
                return render_template('index.html', error=required_percentage)
            else:
                # Format the required percentage as a single value
                required_percentage_formatted = f"{required_percentage:.2f}%"
                return render_template('index.html', result=required_percentage_formatted)
        
        except ValueError:
            error = "Please enter a valid numerical value for Prelim grade."
            return render_template('index.html', error=error)

    return render_template('index.html')

def calculate_required_percentage(prelim_grade):
    passing_grade = 75
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0, 100)

    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

    # Calculate the total contribution of the prelim grade
    current_total = prelim_grade * prelim_weight
    # Determine the total required from midterm and final
    required_total = passing_grade - current_total
    combined_weight = midterm_weight + final_weight

    # Calculate the minimum average percentage required from midterm and final
    min_required_percentage = required_total / combined_weight

    # Ensure it is within the valid range
    if min_required_percentage > 100:
        return "Error: It is not possible to achieve the passing grade with this preliminary score."

    if min_required_percentage < 0:
        min_required_percentage = 0

    return min_required_percentage

if __name__ == '__main__':
    app.run(debug=True)