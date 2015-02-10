# GPG Integration Pack

Pack which allows integration with [GnuPG](https://www.gnupg.org/).

## Requirements

For this pack to work you need to have access to a compatible version of the
GnuGP executable.

## Configuration

* ``gpgbinary`` - Optional path to the gpg binary to use.
* ``gpghome`` - Optional path to gpg keyring home. If not provided,
  ``~/.gnupg`` is used as a default.
* ``debug`` - True to enable debug mode.

## Actions

* ``list_keys`` - List all the keys in the keyring.
* ``import_keys`` - Import ASCII formatted keys from the provided file.
* ``encrypt_file`` - Encrypt a file using asymmetric encryption for the
  provided recipient. Note: Public part of the recipient keys for which you
  are encrypting the file for need to already be available in the gpg keyring.
* ``decrypt_file`` - Action which decrypts asymetrically encrypted file. Note:
  The private part of the key which was used to encrypt the file must already
  be  available in the gpg keyring.
