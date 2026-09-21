#!/usr/bin/env python3
"""Unit tests for the Meta ads operator: the bank reader, the naming and the CPA math.

    python3 -m unittest discover -s tests

Nothing here reaches Meta and nothing here needs `requests`, because every path this
file tests -- the bank, the names, the plan arithmetic, the kill line -- is offline.
"""

import datetime
import json
import pathlib
import sys
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import message_bank  # noqa: E402
import meta_ads  # noqa: E402
import meta_ads_graph as api  # noqa: E402

BANK = ROOT / "docs" / "ads" / "messages.yaml"

SMALL = """\
# a bank with one family and two messages, indented like the real one
landing: https://miamicontactimprov.com/start
identities:
  - climbers
  - yogis
families:
  movement:
    label: Movement and curiosity
    identities:
      - climbers
      - yogis
    body: |
      First paragraph.

      Second paragraph, with a colon: and a URL https://example.com/x.
    messages:
      - slug: move-without-choreography
        identity: climbers
        headline: What happens when two people move without choreography?
        subline: Weight, momentum and one rolling point of contact.
      - slug: the-part-you-cannot-do-alone
        identity: yogis
        headline: The part of a practice you cannot do alone.
        subline: Contact Improvisation, seven to nine in the evening.
"""

class Bank(unittest.TestCase):
    def small(self, text=SMALL):
        path = pathlib.Path(self._tmp()) / "messages.yaml"
        path.write_text(text, encoding="utf-8")
        return message_bank.load(path)

    def _tmp(self):
        import tempfile
        return tempfile.mkdtemp()

    def test_scalars_lists_maps_and_comments(self):
        bank = self.small()
        self.assertEqual(bank["landing"], "https://miamicontactimprov.com/start")
        self.assertEqual(bank["identities"], ["climbers", "yogis"])
        self.assertEqual(bank["families"]["movement"]["label"], "Movement and curiosity")

    def test_block_scalars_keep_their_paragraphs_and_their_colons(self):
        body = self.small()["families"]["movement"]["body"]
        self.assertEqual(body, "First paragraph.\n\nSecond paragraph, with a colon: and a "
                               "URL https://example.com/x.")

    def test_a_list_of_maps_becomes_a_list_of_dicts(self):
        messages = self.small()["families"]["movement"]["messages"]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["slug"], "move-without-choreography")
        self.assertEqual(messages[1]["identity"], "yogis")
        self.assertTrue(messages[0]["headline"].endswith("without choreography?"))

    def test_the_real_bank_has_four_families_of_three_messages(self):
        bank = message_bank.load(BANK)
        families = bank["families"]
        self.assertEqual(sorted(families), ["anxiety", "exercise", "movement", "social"])
        for name, spec in families.items():
            self.assertEqual(len(spec["messages"]), 3, name)
            self.assertGreaterEqual(len(spec["body"].split()), 100, name)
            for message in spec["messages"]:
                self.assertIn(message["identity"], bank["identities"])
                self.assertIn(message["identity"], spec["identities"])

    def test_quotes_and_flow_collections_are_refused_not_guessed(self):
        for bad in ('landing: "quoted"\n', "landing: [a, b]\n", "landing: >\n  folded\n"):
            with self.assertRaises(message_bank.BankError):
                self.small(bad)



class Naming(unittest.TestCase):
    def test_ad_name_is_the_documented_shape(self):
        self.assertEqual(
            meta_ads.ad_name("movement", "new to Miami", "feed", datetime.date(2026, 9, 21)),
            "ci_movement_new-to-miami_feed_20260921")

    def test_identity_words_with_spaces_become_one_hyphenated_word(self):
        self.assertEqual(meta_ads.slug("acro people"), "acro-people")
        self.assertEqual(meta_ads.slug("New  to  Miami!"), "new-to-miami")

    def test_names_are_unique_across_family_identity_format_and_day(self):
        day = datetime.date(2026, 9, 21)
        names = {meta_ads.ad_name(f, i, fmt, day)
                 for f in ("movement", "touch") for i in ("climbers", "actors")
                 for fmt in meta_ads.FORMATS}
        self.assertEqual(len(names), 8)

    def test_creative_name_extends_the_ad_name(self):
        self.assertEqual(meta_ads.creative_name("touch", "couples", "story"),
                         meta_ads.ad_name("touch", "couples", "story") + "_creative")



class Budget(unittest.TestCase):
    def test_dollars_become_subunits(self):
        self.assertEqual(api.minor_units(40), 4000)
        self.assertEqual(api.minor_units(12.5), 1250)

    def test_zero_or_negative_is_refused_rather_than_sent(self):
        for bad in (0, -5):
            with self.assertRaises(SystemExit):
                api.minor_units(bad)



class Plan(unittest.TestCase):
    def bank(self):
        return message_bank.load(BANK)

    def test_the_real_bank_and_the_real_posters_make_twenty_four_ads(self):
        rows, missing = meta_ads.targets(self.bank())
        self.assertEqual(len(rows) + len(missing), 24)
        self.assertEqual(len(rows), 24, "render the posters first: tools/ad_statics.py")

    def test_a_missing_poster_is_named_and_left_out(self):
        rows, missing = meta_ads.targets(self.bank(), exists=lambda path: False)
        self.assertEqual((len(rows), len(missing)), (0, 24))

    def test_every_row_has_the_copy_the_creative_needs(self):
        rows, _ = meta_ads.targets(self.bank())
        for row in rows:
            self.assertTrue(row["headline"] and row["subline"] and row["body"])
            self.assertIn(f"utm_content={row['name']}", row["link"])
            self.assertIn("utm_campaign=ci_fundamentals", row["link"])
            self.assertIn(f"h={row['family']}", row["link"])
            self.assertTrue(row["png"].is_file())

    def test_launch_list_is_two_objects_plus_three_calls_per_ad(self):
        rows, _ = meta_ads.targets(self.bank())
        requests = meta_ads.launch_requests("123", rows, 40)
        self.assertEqual(len(requests), 2 + 3 * len(rows))
        self.assertEqual({r["method"] for r in requests}, {"POST"})
        self.assertEqual([r["path"] for r in requests[:2]],
                         ["/v26.0/act_123/campaigns", "/v26.0/act_123/adsets"])
        self.assertEqual([r["path"].split("/")[-1] for r in requests[2:5]],
                         ["adimages", "adcreatives", "ads"])

    def test_the_account_prefix_is_added_once(self):
        self.assertEqual(api.act_id("123"), "act_123")
        self.assertEqual(api.act_id("act_123"), "act_123")
        self.assertEqual(api.campaign_request("act_123", 40)["path"],
                         "/v26.0/act_123/campaigns")

    def test_every_created_object_is_paused(self):
        rows, _ = meta_ads.targets(self.bank())
        statuses = {}
        for request in meta_ads.launch_requests("123", rows, 40):
            # Images and creatives carry no status of their own: the ad is what gets
            # paused, and the creative only reaches Meta through a paused ad.
            params = request.get("params") or {}
            statuses[request["path"].split("/")[-1]] = params.get("status")
        self.assertEqual(statuses["campaigns"], "PAUSED")
        self.assertEqual(statuses["adsets"], "PAUSED")
        self.assertEqual(statuses["ads"], "PAUSED")
        self.assertIsNone(statuses["adcreatives"])

    def test_each_ad_points_at_its_own_creative(self):
        rows, _ = meta_ads.targets(self.bank())
        requests = meta_ads.launch_requests("123", rows, 40)
        creatives = [r for r in requests if r["path"].endswith("/adcreatives")]
        ads = [r for r in requests if r["path"].endswith("/ads")]
        self.assertEqual(len(creatives), len(rows))
        self.assertEqual(len(ads), len(rows))
        for ad, creative in zip(ads, creatives):
            placeholder = json.loads(ad["params"]["creative"])["creative_id"]
            self.assertEqual(placeholder, f"<CREATIVE_ID:{ad['params']['name']}>")
            self.assertEqual(creative["params"]["name"],
                             f"{ad['params']['name']}_creative")
            self.assertEqual(ad["params"]["status"], "PAUSED")

    def test_the_campaign_carries_the_budget_and_the_ad_set_does_not(self):
        rows, _ = meta_ads.targets(self.bank())
        campaign, adset = meta_ads.launch_requests("act123", rows, 40)[:2]
        self.assertEqual(campaign["params"]["daily_budget"], "4000")
        self.assertNotIn("daily_budget", adset["params"])

    def test_targeting_is_broad_and_the_geo_is_the_studio(self):
        rows, _ = meta_ads.targets(self.bank())
        adset = meta_ads.launch_requests("act123", rows, 40)[1]
        targeting = json.loads(adset["params"]["targeting"])
        self.assertEqual(targeting["geo_locations"]["custom_locations"][0]["radius"], 25)
        self.assertEqual((targeting["age_min"], targeting["age_max"]), (21, 60))
        self.assertEqual(targeting["publisher_platforms"], ["facebook", "instagram"])

    def test_the_creative_carries_the_link_the_hash_and_the_body(self):
        rows, _ = meta_ads.targets(self.bank())
        row = rows[0]
        creative = api.creative_request(row, "act123", "hash123")
        story = json.loads(creative["params"]["object_story_spec"])
        self.assertEqual(story["link_data"]["image_hash"], "hash123")
        self.assertEqual(story["link_data"]["link"], row["link"])
        self.assertEqual(story["link_data"]["message"], row["body"])
        self.assertEqual(story["link_data"]["name"], row["headline"])
        self.assertIn("page_id", story)

    def test_render_shows_the_verb_the_path_and_the_body(self):
        line = api.render(api.campaign_request("act_123", 40))
        self.assertTrue(line.startswith("POST /v26.0/act_123/campaigns"))
        self.assertIn("name=ci_fundamentals", line)
        self.assertIn("daily_budget=4000", line)

    def test_render_names_a_poster_and_its_size_instead_of_its_bytes(self):
        poster = sorted((ROOT / "docs" / "ads" / "out").rglob("*.png"))[0]
        line = api.render({"method": "POST", "path": "/v26.0/act_123/adimages",
                           "files": {"bytes": poster}})
        self.assertIn(f"files[bytes]={poster.name}", line)
        self.assertIn("bytes)", line)

    def test_a_long_body_is_cut_and_marked(self):
        line = api.render({"method": "POST", "path": "/x", "params": {"message": "y" * 400}})
        self.assertTrue(line.endswith("..."))
        self.assertLess(len(line), 340)



class Table(unittest.TestCase):
    def row(self, **overrides):
        base = {"ad_id": "1", "ad_name": "ci_x", "spend": "100.00",
                "inline_link_clicks": "20", "impressions": "900"}
        base.update(overrides)
        return base

    def counts(self, **overrides):
        entry = {"signups": 2, "registrations": 1, "attended": 1}
        entry.update(overrides)
        return {"ci_x": entry}

    def test_unknown_counts_are_not_rendered_as_zeros(self):
        cells = meta_ads.cells_for(self.row(), {})
        self.assertEqual(cells[4], "-1")  # signups: we do not know
        self.assertEqual(cells[8], "-1")  # attended: we do not know
        self.assertEqual(cells[3].strip(), "5.00")

    def test_our_counts_fill_the_last_columns(self):
        cells = meta_ads.cells_for(self.row(), self.counts())
        self.assertEqual([cells[i].strip() for i in (4, 6, 8)], ["2", "1", "1"])
        self.assertEqual([cells[i].strip() for i in (5, 7, 9)],
                         ["50.00", "100.00", "100.00"])
        self.assertEqual(cells[-1].strip(), "100.00")  # cost per attendee decides

    def test_graph_numbers_arrive_as_strings_and_missing_ones_as_zero(self):
        row = {"spend": "12.34", "inline_link_clicks": "7", "impressions": ""}
        self.assertEqual(meta_ads.fetched(row, "spend"), 12.34)
        self.assertEqual(meta_ads.fetched(row, "impressions"), 0.0)
        self.assertEqual(meta_ads.fetched({}, "spend"), 0.0)

    def test_money_prints_a_dash_for_not_a_number(self):
        self.assertEqual(meta_ads.money(None).strip(), "-")
        self.assertEqual(meta_ads.money(3.5).strip(), "3.50")

    def test_the_digest_names_the_winner_and_the_spend(self):
        text = meta_ads.digest([self.row()], self.counts(), 100.0, 40, 60)
        self.assertIn("$100.00", text)
        self.assertIn("ci_x", text)
        self.assertIn("per attendee", text)

    def test_the_digest_flags_an_ad_past_the_line(self):
        text = meta_ads.digest([self.row(spend="300.00")], {}, 300.0, 40, 60)
        self.assertIn("over the line: ci_x", text)

    def test_the_digest_says_so_when_there_is_nothing_to_compare(self):
        text = meta_ads.digest([self.row(spend="5.00")], {}, 5.0, 40, 60)
        self.assertIn("no attendees yet", text)



class WriteGate(unittest.TestCase):
    def test_without_live_nothing_is_allowed(self):
        allowed, why = api.write_allowed(False)
        self.assertFalse(allowed)
        self.assertIn("--live", why)

    def test_with_live_but_no_token_nothing_is_allowed(self):
        with mock.patch.object(api, "secret", return_value=None):
            allowed, why = api.write_allowed(True)
        self.assertFalse(allowed)
        self.assertIn(api.TOKEN_SECRET, why)

    def test_with_live_and_a_token_the_write_is_allowed(self):
        with mock.patch.object(api, "secret", return_value="value"):
            self.assertTrue(api.write_allowed(True)[0])

    def test_presence_is_reported_and_no_value_ever_is(self):
        secret_value = "s3cr3t-do-not-print"
        with mock.patch.object(api, "secret",
                               side_effect=lambda name: secret_value if name ==
                               api.TOKEN_SECRET else None):
            line = api.secret_report()
        self.assertIn(f"{api.TOKEN_SECRET}=present", line)
        self.assertIn(f"{api.PAGE_SECRET}=missing", line)
        self.assertNotIn(secret_value, line)

    def test_a_failed_read_is_missing_rather_than_an_exception(self):
        with mock.patch.object(api.subprocess, "run", side_effect=OSError("no doppler")):
            api._SECRETS.clear()
            self.assertIsNone(api.secret("NOT_A_REAL_SECRET"))


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
