# Mocking & Test Doubles

## MOCK-001: External Dependencies

**Isolate from databases, APIs, file systems.**

```typescript
import { vi } from 'vitest';
import { fetchUserData } from './api';

vi.mock('./api', () => ({
  fetchUserData: vi.fn(),
}));

it('should process user data', async () => {
  vi.mocked(fetchUserData).mockResolvedValue({
    id: '1', name: 'Alice',
  });

  const result = await processUser('1');
  expect(result.greeting).toBe('Hello, Alice!');
});
```

## MOCK-002: Stub vs Mock vs Spy

```typescript
// Stub: Returns canned data
const stubRepo = {
  findById: () => ({ id: '1', name: 'Test' }),
};

// Mock: Verifies interactions
const mockRepo = { save: vi.fn() };
service.createUser(data);
expect(mockRepo.save).toHaveBeenCalledWith(
  expect.objectContaining({ name: 'Alice' })
);

// Spy: Wraps real implementation
const spy = vi.spyOn(realRepo, 'findById');
await service.getUser('1');
expect(spy).toHaveBeenCalledWith('1');
```

## MOCK-003: Avoid Over-Mocking

```typescript
// BAD: Testing the mock
it('should add numbers', () => {
  const mockAdd = vi.fn().mockReturnValue(5);
  expect(mockAdd(2, 3)).toBe(5);
});

// GOOD: Mock only external dependencies
it('should save processed data', async () => {
  const mockDb = { save: vi.fn().mockResolvedValue({ id: '1' }) };
  const service = new DataService(mockDb);

  const result = await service.processAndSave({ value: 42 });

  expect(result.processed).toBe(true);  // Real logic
  expect(mockDb.save).toHaveBeenCalled();  // Side effect
});
```

## MOCK-004: Reset Between Tests

```typescript
describe('UserService', () => {
  const mockRepo = { findById: vi.fn() };

  beforeEach(() => {
    vi.clearAllMocks();  // Reset call history
  });

  afterEach(() => {
    vi.resetAllMocks();  // Reset implementations
  });
});
```

---

## Python Mocking

```python
import pytest

@pytest.fixture
def mock_api(mocker):
    mock = mocker.patch('module.external_api')
    mock.fetch.return_value = {'data': 'test'}
    return mock

def test_with_mock(mock_api):
    result = process_data()
    mock_api.fetch.assert_called_once()
```

## Go Mocking

```go
type UserRepository interface {
    FindByID(id string) (*User, error)
}

type MockUserRepo struct {
    FindByIDFunc func(id string) (*User, error)
}

func (m *MockUserRepo) FindByID(id string) (*User, error) {
    return m.FindByIDFunc(id)
}

func TestGetUser(t *testing.T) {
    mockRepo := &MockUserRepo{
        FindByIDFunc: func(id string) (*User, error) {
            return &User{ID: id, Name: "Alice"}, nil
        },
    }
    service := NewUserService(mockRepo)
    user, _ := service.GetUser("1")
    if user.Name != "Alice" {
        t.Error("expected Alice")
    }
}
```
