# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [0.4.6](https://github.com/sns-sdks/python-youtube/compare/v0.4.5...v0.4.6) (2019-12-01)


### Features

* **api:** :sparkles: add api for get comment by id and test ([6ad1b54](https://github.com/sns-sdks/python-youtube/commit/6ad1b54a7b2a6280b86c7e3df9c04227ae27082d))
* **api:** :sparkles: add api for get comment threads by filter and test. ([d1b41e2](https://github.com/sns-sdks/python-youtube/commit/d1b41e2df8bbe307a1d905570eeae741c7106ce6))
* **api:** :sparkles: add api for get comments by parent and tests ([1545f1a](https://github.com/sns-sdks/python-youtube/commit/1545f1a6ed7d6cf4436521248e3dbf6c9fd23dd1))
* **api:** :sparkles: add api for get guide categories by id or region and test ([f2e4e9a](https://github.com/sns-sdks/python-youtube/commit/f2e4e9a77a3fac236272032e06987fb0334d37c1))
* **api:** :sparkles: add api for get video categories by id or region and test ([e69234b](https://github.com/sns-sdks/python-youtube/commit/e69234b9455251011848493650d7a45d9dd6f451))
* **api:** :sparkles: add comment thread get by id ([3d30162](https://github.com/sns-sdks/python-youtube/commit/3d301622b6554bf2e5a373ebd861ffc1a35993e6))
* **channels:** :sparkles: modify channels and tests ([962fcbd](https://github.com/sns-sdks/python-youtube/commit/962fcbd432b4170891a95c3219f2ce7490ae551a))
* **check:** :recycle: use function to check and convert some parameters. ([ce3b4ec](https://github.com/sns-sdks/python-youtube/commit/ce3b4ec4ba19c41589c7bc1d54061bfa2bfb56d1))
* **decorators:** :sparkles: Add params check decorators and tests. ([6ffaaa7](https://github.com/sns-sdks/python-youtube/commit/6ffaaa780906cc980da0a16c15f21e732ac75c8b))
* **error:** :sparkles: add error repr and str show. ([a7cdcf7](https://github.com/sns-sdks/python-youtube/commit/a7cdcf748d728c26e9666dee3c37347af9983d6a))
* **exception:** :recycle: modify exception implementation ([cf09292](https://github.com/sns-sdks/python-youtube/commit/cf09292bbcc0053f51134a23e479642264ee60e4))
* **model:** :recycle: use BaseResource to provide common field for different resource. ([e1ee35e](https://github.com/sns-sdks/python-youtube/commit/e1ee35e262ef16997c0ae95f5c5c12194166a7ab))
* **model:** :sparkles: add channel retrieve response model. ([a87db07](https://github.com/sns-sdks/python-youtube/commit/a87db073b29d7e0a7e0a021e1b8aff447029c74a))
* **model:** :sparkles: add comment and comment thread api response model. ([dd8978a](https://github.com/sns-sdks/python-youtube/commit/dd8978a055b14dc33bfe5e8e8b27e88f488ac713))
* **model:** :sparkles: add new model for comment and comment thread and tests. ([1beed25](https://github.com/sns-sdks/python-youtube/commit/1beed2500aa832dcaab21ddd5553b29dc290b65f))
* **model:** :sparkles: add new playlist item models and tests. ([2f6d19c](https://github.com/sns-sdks/python-youtube/commit/2f6d19cdd82019a1a21e73c4bc5d2474071828d5))
* **model:** :sparkles: add video and guide category response model and test ([2eb7124](https://github.com/sns-sdks/python-youtube/commit/2eb712456f76f69cddec87cde7dcab5da9d1c3c4))
* **model:** :star2: add new category model ([a48000b](https://github.com/sns-sdks/python-youtube/commit/a48000bc0a7a3a3b8e6341f60ee3b869d2f042fe))
* **OAuth:** :sparkles: fix OAuth workflow. ([3620e5a](https://github.com/sns-sdks/python-youtube/commit/3620e5afa2c8d3ff282c9f94557888c581b8e9f8))
* **param:** :sparkles: add new decorator to transfer comma-separated type. ([85cdf20](https://github.com/sns-sdks/python-youtube/commit/85cdf204092d54675b1f2b4d9e7e19ef9cf4702c))
* **playlistitem:** :sparkles: PlaylistItem Api response model and test ([da1e0ef](https://github.com/sns-sdks/python-youtube/commit/da1e0ef199b46aa6fcb793d3d90f0a4c7efde229))
* **playlistItem:** :sparkles: add new playlist item retrieve api. ([ebaefd9](https://github.com/sns-sdks/python-youtube/commit/ebaefd9e7bcb50a015f0af3c5758c1a1b50e6861))
* **playlists:** :sparkles: Modify playlist api, by playlist id or use channel or mine retrieve data ([afc61d7](https://github.com/sns-sdks/python-youtube/commit/afc61d741bec5ff8c7a5cf20473c9db571f33869))
* **video:** :sparkles: add video list response model and test. ([bc37300](https://github.com/sns-sdks/python-youtube/commit/bc373002d3aa89a245a7083cdeb3ba2e06d1b0b6))
* **videos:** :sprakles: add new api for retrieve videos, by id, chart, myrating. ([519ad96](https://github.com/sns-sdks/python-youtube/commit/519ad9679915cc4a4e178fa57a4121c30218c266))


### Bug Fixes

* **autodoc:** :green_heart: add the new module mock for autodoc. ([ae6aaa5](https://github.com/sns-sdks/python-youtube/commit/ae6aaa5a9ea4e7a7b655c5bc745ded292588c8aa))
* **ci:** let ci run. ([73fa996](https://github.com/sns-sdks/python-youtube/commit/73fa996523ba1d7ce3c446c081a5cff4562c8749))
* **name:** :ambulance: modify old models name to let tests run correct. ([335ee74](https://github.com/sns-sdks/python-youtube/commit/335ee748d3494b216c2875296d638e13ca06eff5))
* **tool:** :fire: remove quota calc, because it is unuseful now. ([c5f1a9c](https://github.com/sns-sdks/python-youtube/commit/c5f1a9c692d838cfdd1b1e0138bc6262f511f482))
* **typo:** :pencil: fix annotations in code. ([c048dd5](https://github.com/sns-sdks/python-youtube/commit/c048dd5a85c880ec463cd17b2ab1e886bc0dbb46))
