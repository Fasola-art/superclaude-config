# Auto-generate Tests

Analyze code files and automatically generate tests.

## Usage
```
/generate-tests <file-path>
/generate-tests src/utils/helper.ts
```

---

**Execution Instructions:**

1. Read and analyze the specified file
2. Generate test cases for each function/class
3. Use appropriate test framework for the language:
   - TypeScript/JavaScript: Jest or Vitest
   - Python: pytest
   - Go: testing package

4. Test file output location:
   - `src/utils/helper.ts` → `src/utils/helper.test.ts`
   - `lib/calc.py` → `tests/test_calc.py`

5. Include these test types:
   - Happy path (normal cases)
   - Edge cases (empty values, null, boundary values)
   - Error cases (exception handling)

6. After writing test file, execute to verify
