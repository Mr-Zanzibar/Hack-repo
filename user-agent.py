from user_agents import parse

ua_string = input("Enter the User-Agent string: ")

if ua_string != '':
  
    try:
        user_agent = parse(ua_string) # This script allows to test the User Agent library and theck if the User agent is valid and if it is a bot.
        print(f"[+] The user agent is: {user_agent}")
        print(f"[+] The user is bot: {user_agent.is_bot}")

    except Exception as e:
        print(f"[-] Error parsing the User-Agent: {e}")

else:
    exit("[-] Please enter a valid string.")
