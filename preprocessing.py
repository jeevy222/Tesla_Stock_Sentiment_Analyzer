import re
import pandas as pd


# cleaning of the tesla content
def clean_content_and_save_to_csv():
    """clean tesla content and save processed data in processed content csv."""
    clean_tesla_content = []
    # link_remove = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    # url_remove = r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    tesla_content_df = pd.read_csv('tesla_content.csv')
    for content in tesla_content_df.tesla_content:
        if (type(content) == str) and (len(content.strip()) > 0):
            # Remove links that start with HTTP/HTTPS in the content
            content = re.sub(
                r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',
                '',
                content, flags=re.MULTILINE)


            # Remove other url links
            content = re.sub(r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '',
                             content, flags=re.MULTILINE)

            # Remove hashtags
            content = re.sub(r"#(\w+)", ' ', content, flags=re.MULTILINE)
            # Remove Mentions
            content = re.sub(r"@(\w+)", ' ', content, flags=re.MULTILINE)
            # Remove multiple spaces
            content = re.sub(' +', ' ', content, flags=re.MULTILINE)
            # Remove digits
            content = re.sub(r"\d", "", content)
            # Change to lower case
            content = content.lower()
            # Strip the content
            content = content.strip()
            print(content)
            clean_tesla_content.append(content)

    clean_tesla_content_df = pd.DataFrame(columns=['processed_content'], data=clean_tesla_content)
    clean_tesla_content_df.to_csv('tesla_processed_content.csv', index=False)
    print('Total Processed Articles for Tesla: ', len(clean_tesla_content))


if __name__ == '__main__':
    print('---Pre process tesla content---')
    clean_content_and_save_to_csv()
