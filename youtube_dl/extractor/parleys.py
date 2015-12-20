# coding: utf-8

from __future__ import unicode_literals

from common import InfoExtractor


# parleys support ticket: https://github.com/rg3/youtube-dl/issues/1876
# multipart video download support which might block this: https://github.com/rg3/youtube-dl/pull/5217

# TODO
# ParleysChannelIE https://api.parleys.com/api/presentations.json/<channel_id>
# ParleysSpeakerIE https://api.parleys.com/api/presentations.json/speaker/<speaker_id>

class ParleysIE(InfoExtractor):
    _VALID_URL = r'https?://www\.parleys\.com/tutorial/(?P<id>[^/]+)'
    _PRESENTATION_API_ENDPOINT = 'https://api.parleys.com/api/presentation.json/%s'
    # https://api.parleys.com/api/presentation.json/<presentation_id>

    def _real_extract(self, url):
        video_id = self._match_id(url)
        presentation_api_url = self._PRESENTATION_API_ENDPOINT % video_id
        details = self._download_json(presentation_api_url, video_id)
        _title = details['title']

        return {
            'id': video_id,
            'title': _title,

        }

    def _parse_assets(self, details):
        multiparts = [
            self._extract_from_asset_files(asset)
            for asset in details['assets']
            if asset['target'] == 'STREAM'
        ]
        return multiparts

    def _extract_from_asset_files(self, asset):
        return [
            {
                'url': file['httpDownloadURL'],
                'fileName': file['fileName'],
                'format': file['format'],
                'fileSize': file['fileSize'],
            }
            for file in asset['files']
        ]
