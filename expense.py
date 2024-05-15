class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name = name
        self.category = category
        self.amount = amount
    def __repr__(self):
        return f"Expense(name={self.name}, amount={self.amount}, category={self.category})"

    
