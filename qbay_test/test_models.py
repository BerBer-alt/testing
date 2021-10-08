from qbay.models import Product, register, login, update_product, update_profile


def test_r1_7_user_register():
    '''
    Testing R1-7: If the email has been used, the operation failed.
    '''

    assert register('u0', 'test0@test.com', '123456') is True
    assert register('u0', 'test1@test.com', '123456') is True
    assert register('u1', 'test0@test.com', '123456') is False


def test_r2_1_login():
    '''
    Testing R2-1: A user can log in using her/his email address 
      and the password.
    (will be tested after the previous test, so we already have u0, 
      u1 in database)
    '''

    user = login('test0@test.com', 123456)
    assert user is not None
    assert user.username == 'u0'

    user = login('test0@test.com', 1234567)
    assert user is None

def test_r3_1_update_user_profile():
  '''
  Testing R2-1: A user is only able to update 
  his/her user name, shipping_address, and postal_code.
  '''

  assert update_profile('Tom', '123 University Ave', 'K7L 0Y3') is True

def test_r3_2_update_user_profile():
  '''
  R3-2: Shipping_address should be non-empty, 
  alphanumeric-only, and no special characters such as !
  '''
  assert update_profile('Tom', '', 'K7L 0Y3') is False
  assert update_profile('Tom', '123! University Ave', 'K7L 0Y3') is False

def test_r3_3_update_user_profile():
  '''
  R3-3: Postal code has to be a valid Canadian postal code
  '''

  assert update_profile('Tom', '123 University Ave', 'K0Y3') is False

def test_r3_4_update_user_profile():
  '''
  R3-4: User name follows the requirements above
  '''

  assert update_profile('m', '123 University Ave', 'K7L 0Y3') is False
  assert update_profile('qwertyuiopasdfghjklz', 
                        '123 University Ave', 'K7L 0Y3') is False
  assert update_profile('', '123 University Ave', 'K7L 0Y3') is False
  assert update_profile(' Tim ', '123 University Ave', 'K7L 0Y3') is False


def test_r5_1_update_product():
  '''
  R5-1: One can update all attributes of the product, 
  except owner_email and last_modified_date
  '''
  # product = create_product('apple', 'This is a description', 
  # 1, '2021-10-07','aa12a@queensu.ca')
  assert update_product(1234, "apple", 
                        "an apple a day keeps doctor away", 3) is True

def test_r5_2_update_product():
  '''
  R5-2: Price can be only increased but cannot be decreased
  '''
  # product = create_product('apple', 'This is a description', 
  # 100, '2021-10-07','aa12a@queensu.ca')
  assert update_product(1234, "apple", 
                        "good for health", 1) is False

def test_r5_3_update_product():
  '''
  R5-3: last_modified_date should be updated when the 
  update operation is successful
  '''

def test_r5_4_update_product():
  '''
  R5-4: When updating an attribute, one has to make sure 
  that it follows the same requirements as above
  '''
