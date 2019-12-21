"""Graphical User Interface for Newton's Method Calculator
Created on Fall 2019
CS108 Project
@author: Jiho Kim (jk249)
"""
from tkinter import Tk, Toplevel, Frame, Label, Entry, Button, OptionMenu, Listbox, Scrollbar, StringVar, END, W, E, N, S, PhotoImage
from numpy import array, sin, cos, tan, arcsin, arccos, arctan, cbrt, sqrt, exp, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from validate import validate
from newton import Newton


class Gui:
    """Gui class for Newton's Method Calculator GUI"""
    def __init__(self, window):
        """This constructor instantiates the GUI for Newton's Method Calculator"""
        # Instantiate Newton's Method Calculator
        self.nt = Newton()  # This class makes sure that appropriate data are passed on to the Newton class

        self.window = window

        # Primary frame for calculator related interactions
        calculator_frame = Frame(self.window)
        calculator_frame.grid(row=0, column=0, padx=10, pady=10)

        # Secondary frame for "f(x)" related interactions
        f_frame = Frame(calculator_frame)
        f_frame.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        # Display "f(x) = "
        f_label = Label(f_frame, text="f(x) = ")
        f_label.grid(row=0, column=0, sticky=W)

        self.f = StringVar()
        self.f.set("")

        # Entry for "f(x) = "
        self.f_entry = Entry(f_frame, textvariable=self.f, width=35)
        self.f_entry.grid(row=0, column=1)

        # Secondary frame for "f'(x)" related interactions
        f_prime_frame = Frame(calculator_frame)
        f_prime_frame.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        # Display "f'(x) = "
        f_prime_label = Label(f_prime_frame, text="f'(x) = ")
        f_prime_label.grid(row=0, column=0, sticky=W)

        self.f_prime = StringVar()

        # Display the result of the differentiation
        f_prime_label = Label(f_prime_frame, textvariable=self.f_prime)
        f_prime_label.grid(row=0, column=1, sticky=W)

        # Secondary frame for "Initial solution x0 = " related interactions
        init_solution_frame = Frame(calculator_frame)
        init_solution_frame.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        # Display "Initial solution x0 = "
        init_solution_label = Label(init_solution_frame, text="Initial solution (x\u2080) = ")
        init_solution_label.grid(row=0, column=0, sticky=W)

        self.init_solution = StringVar()
        self.init_solution.set("")

        # Entry for "Initial solution x0 = "
        self.init_solution_entry = Entry(init_solution_frame, textvariable=self.init_solution, width=5)
        self.init_solution_entry.grid(row=0, column=1, sticky=W)

        # Secondary frame for "Maximum number of iterations (n)" related interactions
        max_iterations_frame = Frame(calculator_frame)
        max_iterations_frame.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        # Display "Maximum number of iterations (n)"
        max_iterations_label = Label(max_iterations_frame, text="Maximum number of iterations (n)")
        max_iterations_label.grid(row=0, column=0)

        # Options for the menu
        self.list_of_iter = ["10", "20", "30", "40", "50", "100", "500"]

        self.selection = StringVar()
        self.selection.set(self.list_of_iter[0])

        # OptionMenu for "Maximum number of iterations (n)"
        max_iter_option = OptionMenu(max_iterations_frame, self.selection, *self.list_of_iter)
        max_iter_option.grid(row=0, column=1)

        # Secondary frame for "Run Newton's Method" related interactions
        execution_frame = Frame(calculator_frame)
        execution_frame.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        # Button for "Run Newton's Method"; executes the calculator
        run_button = Button(execution_frame, text="Run Newton's Method", command=self.run)
        run_button.grid(row=0, column=0)

        # Button for "Reset"; clears all entry and result
        reset_button = Button(execution_frame, text="Reset", command=self.reset)
        reset_button.grid(row=0, column=1, padx=10)

        # Button for "Help"; opens up the documentation
        help_button = Button(execution_frame, text="Help", command=self.help)
        help_button.grid(row=0, column=2)

        # Secondary frame for the results table
        results_frame1 = Frame(calculator_frame)
        results_frame1.grid(row=5, column=0, padx=10, sticky=W)

        # Display the title of the results table
        table_label = Label(results_frame1, text="n          x")
        table_label.grid(row=0, column=0)

        # Secondary frame for the results table (con't)
        results_frame2 = Frame(calculator_frame)
        results_frame2.grid(row=6, column=0, padx=10, pady=10, sticky=W)

        # Scrollbar for the results table
        scrollbar = Scrollbar(results_frame2, command=self.scroll_with_bar)
        scrollbar.grid(row=0, column=2, sticky=E+N+S)

        # Table for the list of n iterations
        self.n_box = Listbox(results_frame2, yscrollcommand=scrollbar.set, width=5)
        self.n_box.grid(row=0, column=0)
        self.n_box.bind("<MouseWheel>", self.scroll_with_wheel)

        # Table for the list of x results
        self.x_box = Listbox(results_frame2, yscrollcommand=scrollbar.set, width=25)
        self.x_box.grid(row=0, column=1)
        self.x_box.bind("<MouseWheel>", self.scroll_with_wheel)

        # Secondary frame for error related interactions
        error_frame = Frame(calculator_frame)
        error_frame.grid(row=7, column=0, padx=10, pady=10, sticky=W)

        self.error_msg = StringVar()
        self.error_msg.set("Welcome to Newton's Method Calculator!")

        error_label = Label(error_frame, textvariable=self.error_msg)
        error_label.grid(row=0, column=0)

        # Primary frame for graphing related interactions
        self.graphing_frame = Frame(self.window)
        self.graphing_frame.grid(row=0, column=1, padx=10)

        # Draw empty graph on the GUI at the start of the program
        self.default_graph()

    def scroll_with_bar(self, *what):
        """This function allows the list boxes to be scrolled with a bar"""
        self.n_box.yview(*what)
        self.x_box.yview(*what)

    def scroll_with_wheel(self, event):
        """This function allows the list boxes to be scrolled with the mouse wheel"""
        self.n_box.yview_scroll(event.delta, "units")
        self.x_box.yview_scroll(event.delta, "units")

    def default_graph(self):
        """This function draws an empty graph"""
        graph = Figure(figsize=(5, 4), dpi=100)
        axes = graph.add_subplot(1, 1, 1)
        
        axes.set_title("f(x)")

        # Embed matplotlib graph on tkinter frame
        canvas = FigureCanvasTkAgg(graph, master=self.graphing_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10)

    def graph(self, expression):
        """This function graphs the user defined f(x)"""
        if validate(expression):
            expr = expression

            # Convert SymPy trigonometric functions to NumPy compatible versions
            if "sec" in expr:
                expr = expr.replace("sec", "1/cos")
            if "csc" in expr:
                expr = expr.replace("csc", "1/sin")
            if "cot" in expr:
                expr = expr.replace("cot", "1/tan")
            if "asin" in expr:
                expr = expr.replace("asin", "arcsin")
            if "acos" in expr:
                expr = expr.replace("acos", "arccos")
            if "atan" in expr:
                expr = expr.replace("atan", "arctan")
        else:
            self.error_msg.set("Sorry! You've entered an invalid function...")

        # Following two lines are adapted from https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_tk_sgskip.html
        graph = Figure(figsize=(5, 4), dpi=100)
        axes = graph.add_subplot(1, 1, 1)
        
        axes.set_title("f(x)")

        x = array(range(-50, 50))

        # FIXME: numpy does not support sympy math; thus, not all functions can be graphed
        # This calculator cannot graph inverse of sec, csc, cot due to lack of support from numpy
        # This calculator cannot graph entered expressions with "root()" or "ln()" in them
        # Current solution: only enter polynomial functions for the best experience with the calculator

        # Catch errors that are raised when matplotlib cannot graph the function

        err = "Sorry! This function can't be graphed yet..."

        try:
            y = eval(expr)
            axes.plot(x, y)
        except TypeError:
            self.error_msg.set(err)
        except NameError:
            self.error_msg.set(err)

        # Embed matplotlib graph on tkinter frame
        # Following three lines are adapted from https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_tk_sgskip.html
        canvas = FigureCanvasTkAgg(graph, master=self.graphing_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10)

    def reset(self):
        """This function clears all entry and result"""
        self.f_entry.delete(0, END)
        self.f_prime.set("")
        self.init_solution_entry.delete(0, END)
        self.selection.set(self.list_of_iter[0])
        self.n_box.delete(0, END)
        self.x_box.delete(0, END)
        self.default_graph()
        self.error_msg.set("Welcome to Newton's Method Calculator!")

    def run(self):
        """This function executes the Newton's Method Calculator"""
        # Reset the tables and the graph for the user, in case if the user has not used the "Reset" button
        self.n_box.delete(0, END)
        self.x_box.delete(0, END)
        self.default_graph()

        # Catch all ValueErrors and display appropriate message on the calculator
        try:
            # Raise ValueError if "f(x) =" entry is missing
            if self.f.get() == "":
                raise ValueError("Please enter the function...")

            # Raise ValueError if "f(x) =" is a constant
            if isinstance(self.f.get(), (int, float)):
                raise ValueError("Sorry! You've entered an invalid function...")

            # Raise ValueError if "Initial solution x0 =" is missing
            if self.init_solution.get() == "":
                raise ValueError("Please enter the initial solution...")

            if self.init_solution.get().isalpha():
                raise ValueError("Initial solution must be a number...")

            # Calculate the derivative and display it as the result of "f'(x) ="
            self.f_prime.set(self.nt.derive(self.f.get()))

            # Approximate using the Newton's Method Calculator
            result = self.nt.newton(
                expression=self.f.get(),
                initial_guess=float(self.init_solution.get()),
                max_iterations=int(self.selection.get())
            )

            # Display the result on the tables
            self.n_box.insert(END, "{n}".format(n=0))
            self.x_box.insert(END, "{x}".format(x=self.init_solution.get()))

            for r in range(len(result)):
                self.n_box.insert(END, "{n}".format(n=r + 1))
                self.x_box.insert(END, "{x}".format(x=result[r]))

            # Graph the expression, if possible
            self.graph(expression=self.f.get())
        except ValueError as err:
            self.error_msg.set(err)

    def help(self):
        """This function opens up a window to display the documentation"""
        second_window = Toplevel(self.window)
        second_window.title("Help")
        second_window.resizable(False, False)

        primary_frame = Frame(second_window)
        primary_frame.grid(row=0, column=0, padx=10, pady=10)

        # "Newton's Method Calculator Documentation"
        welcome_label = Label(primary_frame, text="Newton's Method Calculator Documentation")
        welcome_label.config(font="10")
        welcome_label.grid(row=0, column=0)

        documentation_frame = Frame(primary_frame)
        documentation_frame.grid(row=1, column=0, pady=10)

        documentation_frame2 = Frame(primary_frame)
        documentation_frame2.grid(row=2, column=0)

        documentation_frame3 = Frame(primary_frame)
        documentation_frame3.grid(row=3, column=0, pady=10)

        documentation_frame4 = Frame(primary_frame)
        documentation_frame4.grid(row=4, column=0)

        # "How to enter inverse trigonometric functions"
        label1 = Label(documentation_frame, text="How to enter inverse trigonometric functions:")
        label1.grid(row=1, column=0)
        label2 = Label(documentation_frame, text="arccos(x) must be entered as acos(x)", fg="gray")
        label2.grid(row=2, column=0)
        label3 = Label(documentation_frame, text="arcsin(x) must be entered as asin(x)", fg="gray")
        label3.grid(row=3, column=0)
        label4 = Label(documentation_frame, text="arctan(x) must be entered as atan(x)", fg="gray")
        label4.grid(row=4, column=0)
        label5 = Label(documentation_frame, text="etc...", fg="gray")
        label5.grid(row=5, column=0)

        # "How to enter other mathematical stuff:"
        label6 = Label(documentation_frame2, text="How to enter other mathematical stuff:")
        label6.grid(row=1, column=0)
        label7 = Label(documentation_frame2, text="To use a logarithm, you should enter log(x, base)", fg="gray")
        label7.grid(row=2, column=0)
        label8 = Label(documentation_frame2, text="Instead of x**(1/2), you may enter sqrt(x)", fg="gray")
        label8.grid(row=3, column=0)
        label9 = Label(documentation_frame2, text="Instead of x**(1/3), you may enter cbrt(x)", fg="gray")
        label9.grid(row=4, column=0)
        label10 = Label(documentation_frame2, text="Instead of x**(1/n), you may enter root(x, n)", fg="gray")
        label10.grid(row=5, column=0)
        label11 = Label(documentation_frame2, text="You should enter 'pi' to denote 'π'", fg="gray")
        label11.grid(row=6, column=0)

        # Other notes...
        label12 = Label(documentation_frame3, text="Some functions can't be graphed yet (e.g. acot(x))")
        label12.grid(row=0, column=0)
        label13 = Label(documentation_frame3, text="It would great to overuse parenthesis")
        label13.grid(row=1, column=0)
        label14 = Label(documentation_frame3, text="Implicit multiplication is not supported")
        label14.grid(row=2, column=0)

        # Reminder of the Newton's Method formula
        label15 = Label(documentation_frame4, text="Newton's Method Formula:", fg="grey")
        label15.grid(row=0, column=0)
        formula = PhotoImage(file="formula.png")
        label16 = Label(documentation_frame4, image=formula)
        label16.image = formula
        label16.grid(row=1, column=0)


if __name__ == "__main__":
    root = Tk()
    root.title("Newton's Method Calculator")
    root.resizable(False, False)
    app = Gui(root)
    root.mainloop()
