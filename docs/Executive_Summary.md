# Executive Summary: Package Combination Optimizer

## Business Context
Our supplement company faces a unique challenge in order fulfillment. We offer a single product in various package sizes (10-day, 14-day, 30-day supplies), but customers often request quantities that don't perfectly match these fixed sizes. This mismatch leads to overdelivery, impacting our costs and operational efficiency.


## Problem Statement
Our goal is to identify the largest order quantity that cannot be perfectly fulfilled using any combination of our current package sizes. We consider an order 'perfectly purchasable' when it can be met exactly, without any over or under-delivery, using the available package size options.

Given the dynamic nature of our package size offerings, which are subject to frequent changes based on market trends and supplier availability, we require a flexible and adaptable solution. The ideal approach should be able to seamlessly accommodate variations in package sizes and quickly recalculate the maximum unfulfillable order quantity whenever changes occur.

By tackling this problem head-on, we position ourselves to make data-driven decisions that optimize our packaging strategy, streamline our operations, and ultimately enhance the customer experience while driving business growth.


## Problem Analysis
Our challenge maps directly to the Frobenius Coin Problem, a well-known mathematical problem. This mapping revealed that the problem is NP-Complete when package sizes share common factors and becomes NP-Hard when package sizes are coprime.

To make the problem solvable, we will narrow the scope to the NP-Hard context, requiring that all given package sizes together have a Greatest Common Divisor (GCD) of 1, though individual pairs can share factors. For example, {6, 10, 15} is a valid set, as pairs share factors, but their GCD is 1.

This approach enables us to build a tool that effectively addresses common packaging scenarios while maintaining computational feasibility.

## Algorithm Selection

We've chosen the **Round Robin Algorithm** for finding the largest unfulfillable order size. Here's why it works well for our package fulfillment challenge:

### Core Benefits
- **Fast Processing**: Performance scales linearly in O(ka₁) (k = number of packages, a₁ = single package size)
- **Memory Efficient**: Uses minimal computer memory O(a₁)
- **Complete Coverage**: Systematically finds all possible package combinations
- **Guaranteed Accuracy**: Never misses a valid solution
- **Easy Updates**: Simple to modify when adding new package sizes


### How It Works

The Round Robin Algorithm uses a powerful insight to solve our package fulfillment challenge efficiently. Instead of tracking every possible order size, we create a table with n entries (where n is the size of a chosen package in the given set, say 5). This table tracks only the smallest achievable order size for each possible remainder of our chosen package (for 5, the possible remainders are 0,1,2,3,4). This compact tracking works because of a key property: if we can fulfill an order size M, we can always fulfill size M plus our chosen package size by adding one more package. The algorithm then systematically updates this table with each new package size, progressively discovering all possible combinations while only tracking n numbers instead of infinite possibilities.


#### Example Walkthrough

Let's see exactly how we find our answer with package sizes of 5-day, 8-day, 9-day servings:

**Step 1: Initialize with 5-serving package**

We first by create a table of size 5 (because 5 has remainder 0,1,2,3,4) for order sizes that can be fulfilled. Then we start by the algorithm by seeding our table using our first package size (5 days). With a single package size of 5, we can only fulfill orders in multiples of 5, so 0 is the only package size we can achieve with 1 5-day package. All other sizes ar marked as impossible to fulfill perfectly

```
Initial Table:
Remainder when divided by 5: [0, 1, 2, 3, 4]
Smallest achievable size:    [0, ∞, ∞, ∞, ∞]
```

**Step 2: Add 8-serving package**


Next we try our 8-day package size. We take multiples of 8 (8, 16, 24, 32) and attempt to update the residue table.

```
Process: Start with 8 and keep adding 8s for remainder classes
8/5  → remainder 3  → 8  < ∞  → update table
16/5 → remainder 1  → 16 < ∞  → update table
24/5 → remainder 4  → 24 < ∞  → update table
32/5 → remainder 2  → 32 < ∞  → update table

Updated Table:
Remainder when divided by 5: [0, 1, 2, 3, 4]
Smallest achievable size:    [0, 16, 32, 8, 24]
```

**Step 3: Add 9-serving package**
Next we try our p-day package size. We take multiples of 9 (9, 18, 27, 36) and attempt to update the residue table.
```
Process: Start with 9 and keep adding 9s
9/5  → remainder 4  → 9  < 24  → update table
18/5 → remainder 3  → 18 > 8 
27/5 → remainder 2  → 27 < 32  
36/5 → remainder 1  → 36 > 16 

Final Table:
Remainder when divided by 5: [0, 1, 2, 3, 4]
Smallest achievable size:    [0, 16, 27, 8, 9]
```

**4. Finding Our Maximum Gap**
Looking at our final table, we can make any size that has a "path" through our table.

```
Size:      0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25...
Possible?: ✓  ✗  ✗  ✗  ✗  ✓  ✗  ✗  ✓  ✓  ✓  ✗  ✗  ✓  ✓  ✓  ✓  ✓  ✓  ✓  ✓  ✗  ✗  ✓  ✓  ✓...
```

Our largest "gap" in this case is 22. 

**5. The Result**

Instead of manually searching through the table, we can calculate the Frobenius Number by taking the maximum value in our table and subtracting our chosen package (27 - 5 = 22).


### Proof of Convergence

The Round Robin Algorithm is guaranteed to find the correct answer because we can prove it through these key points:

1. **Base Case**: Starting with just one package size, we know exactly what orders we can fulfill (multiples of that package size). This gives us a solid foundation.

2. **Building Up**: When we add each new package size:
   - We only update a value in our table if we find a smaller achievable order size
   - Each update either keeps the current value or improves it
   - Values never get worse (decrease) during updates

3. **Completeness**: For any order size that's possible to fulfill:
   - The algorithm will find it because it systematically tries all combinations of the value's denominations
   - The table always contains the smallest possible way to achieve each remainder
   - No valid combinations are missed

4. **Termination**: The algorithm must finish because:
   - We only make a finite number of updates
   - Each package size is processed exactly once
   - The table size stays fixed based on our chosen package size

Therefore, when the algorithm finishes, our table contains the optimal (smallest) values for each remainder class, giving us a complete picture of what's possible and what isn't.

### Comprehensive Testing

1. Input Validation
   - Empty package lists → None
   - Single package size → None
   - Non-integer package sizes → TypeError

2. Simple Package Combinations
   - [5,14] → 51 (largest unfulfillable order)
   - [10,14,30] → 73

### Edge Cases
1. Package Size Variations
   - Ordering [3,5,7], [7,5,3],[7,5,3] → 4
   - Zero quantities [0,3,5,7], [3,0,5,7], [3,5,7,0] → 4
   - Zeros [0,0,0] → None
   - Duplicate sizes [3,3,5,7] → 4
   - Non Integer [2.5, 3] → TypeError

2. Scale Testing
   - Non-coprime sizes [4,6] → None
   - Large packages [9901,10000,10099] → 49980149
   - Large Non-coprime packages [10000, 20000] → None
   - Many options [101,103,...,173] → 402
   - X-Large packages [1000001,...,1000073] → 27779027777
  
## Business Impact

### Immediate Benefits
1. **Better Order Management**
   - Precise identification of unfulfillable orders
   - Optimal package combinations for every order
   - Significantly reduced overdelivery

2. **Operational Improvements**
   - Data-driven package size decisions
   - Streamlined inventory management
   - Reduced waste

### Long-term Value
1. **Strategic Advantages**
   - Evidence-based package size optimization
   - Simplified operations
   - Enhanced product offerings
   - Better customer satisfaction

2. **Cost Optimization**
   - Minimized overdelivery expenses
   - Optimized shipping
   - Improved inventory efficiency

## Conclusion
The Round Robin Algorithm provides a robust, efficient solution to our package combination challenge. Through comprehensive testing and mathematical verification, we've ensured it handles all possible solvable scenarios reliably. This solution enables us to:
- Make informed decisions about package offerings
- Optimize order fulfillment
- Reduce operational costs
- Improve customer satisfaction

The system is now ready for implementation, with proven reliability across all package size combinations and order volumes.