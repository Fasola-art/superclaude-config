---
description: "TDD 워크플로우 (테스트 우선) | TDD workflow - write tests first, code second"
argument-hint: "[feature-description]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "TodoWrite", "AskUserQuestion"]
---

# TDD Workflow

<tdd-command>

## Core Principles

1. **Test FIRST, code SECOND** - Never write production code without a failing test
2. **Small steps** - Red → Green → Refactor in tiny increments
3. **Use TodoWrite** - Required for tasks with 3+ steps

---

## Phase 1: Understand Requirements

**Actions:**
1. Clarify the feature requirements with the user
2. Identify input/output expectations
3. List edge cases and error scenarios

**Output:**
- Clear understanding of what to implement
- List of test cases to write

---

## Phase 2: Write Failing Test (🔴 Red)

**Actions:**
1. Create test file if not exists
2. Write ONE test that describes expected behavior
3. Run test - verify it FAILS for the right reason

**Template (TypeScript):**
```typescript
describe('FeatureName', () => {
  it('should [expected behavior]', () => {
    // Arrange
    const input = /* test data */;

    // Act
    const result = functionUnderTest(input);

    // Assert
    expect(result).toBe(/* expected */);
  });
});
```

**Template (Python):**
```python
def test_should_expected_behavior() -> None:
    # Arrange
    input_data: str = "test_input"
    expected: str = "expected_output"

    # Act
    result: str = function_under_test(input_data)

    # Assert
    assert result == expected
```

**Template (Go - Table-Driven):**
```go
func TestFeatureName(t *testing.T) {
    tests := []struct {
        name     string
        input    string
        expected string
    }{
        {"valid input", "test", "expected"},
        {"empty input", "", ""},
        {"edge case", "edge", "result"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := FunctionUnderTest(tt.input)
            if result != tt.expected {
                t.Errorf("got %v, want %v", result, tt.expected)
            }
        })
    }
}
```

---

## Phase 3: Implement Minimal Code (🟢 Green)

**Actions:**
1. Write the MINIMUM code to make the test pass
2. Don't over-engineer - just make it work
3. Run test - verify it PASSES

**Rules:**
- Only write code that makes a failing test pass
- Resist the urge to add extra functionality
- If you think of more cases, write them as tests first

---

## Phase 4: Refactor (🔵 Refactor)

**Actions:**
1. Improve code quality while keeping tests green
2. Remove duplication
3. Improve naming and structure
4. Run tests after each change

**Checklist:**
- [ ] No duplicate code
- [ ] Clear function/variable names
- [ ] Single responsibility
- [ ] All tests still pass

---

## Phase 5: Repeat

**Actions:**
1. Pick the next test case
2. Go back to Phase 2
3. Continue until all requirements met

**Summary Output:**

```
## TDD Summary

### Tests Written
- ✅ test_case_1
- ✅ test_case_2
- ✅ test_edge_case

### Implementation
- Created: path/to/file.ts
- Functions: functionName()

### Coverage
- Lines: XX%
- Branches: XX%

### Run Tests
- TypeScript: npm test -- --coverage
- Python: pytest --cov=src
- Go: go test -cover ./...
```

---

## Language Detection

Detect project language and use appropriate:
- **TypeScript**: Jest or Vitest
- **Python**: pytest
- **Go**: testing package

Check for existing test configuration:
- `package.json` → scripts.test
- `pyproject.toml` → [tool.pytest]
- `go.mod` → Go project

---

## Example Workflow

User: "Add a function to validate email addresses"

1. **Understand**: Email validation - check format, common patterns
2. **Red**: Write `test_valid_email_returns_true`
3. **Green**: Implement `isValidEmail()` returning `true` for valid pattern
4. **Refactor**: Clean up regex, add documentation
5. **Red**: Write `test_invalid_email_returns_false`
6. **Green**: Update implementation
7. **Continue**: Edge cases (empty string, special chars, etc.)

</tdd-command>
