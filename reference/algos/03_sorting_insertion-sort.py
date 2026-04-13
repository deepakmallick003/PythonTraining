'''
###Insertion Sort###

Imagine you have a bunch of playing cards in your hand and you want to arrange them in order from the smallest 
to the largest. Here's how you can do it using something called "Insertion Sort":

1) Start with the First Card: You already have one card, so it's automatically in the right spot.
2) Pick the Next Card: Take the next card from the deck.
3) Compare and Insert: Compare this card with the cards already in your hand, starting from the right 
   (the last card you placed). Move the cards in your hand one by one until you find the right spot 
   for the new card.
4) Repeat: Keep doing this until all the cards from the deck are in your hand and sorted.

Here's a simple drawing to help visualize it:
https://upload.wikimedia.org/wikipedia/commons/0/0f/Insertion-sort-example-300px.gif

'''


def insertion_sort(numbers):
    # Loop over the list starting from the second element
    for i in range(1, len(numbers)):
        # Take the current number to be placed correctly
        current_value = numbers[i]
        # Find the position where the number should be inserted
        j = i - 1
        # Move the elements of the list that are greater than current_value to one position ahead of 
        # their current position
        while j >= 0 and numbers[j] > current_value:
            numbers[j + 1] = numbers[j]
            j -= 1
        # Place the current_value at its correct position
        numbers[j + 1] = current_value

# Example usage:
numbers = [12, 11, 13, 5, 6]
print("Original list:", numbers)
insertion_sort(numbers)
print("Sorted list:", numbers)



'''
Time Complexity =>
The time it takes to run the algorithm is O(n²), where n is the number of elements in the list. 
This is because for each element, you might have to compare it with all the other elements. 
So, if you have 10 elements, it might take 10 x 10 = 100 steps in the worst case.

Space Complexity => 
The space complexity is O(1), which means the algorithm only needs a constant amount of extra space, 
regardless of how many elements there are. 
This is because we are sorting the list in place and not using any extra list or array.

Why O(n²) for Time Complexity? =>
In the worst case, for each element, you might have to look at all the previous elements to find its 
correct position. For the first element, you do 1 comparison, for the second element, 
you do 2 comparisons, and so on. This results in a total number of comparisons being roughly n x n, hence O(n²).

Why O(1) for Space Complexity? => 
The algorithm does not require any extra space that grows with the size of the input. 
It sorts the list in place, 
using only a few extra variables. So, the extra space needed is constant, hence O(1).
'''
